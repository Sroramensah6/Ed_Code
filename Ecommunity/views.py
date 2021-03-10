from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.response import Response

from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import RedirectView

from taggit.models import Tag
from News.models import NewsPost

from .models import QuestionModel, QuestionView, Categories, Like, Rate, Answers
from .forms import QuestionForm, AnswerForm

# Community


def get_tag_count():
    queryset = QuestionModel\
        .objects\
        .values('tags__name', 'tags__slug')\
        .annotate(Count('tags__name'))
    return queryset


def get_category_count():
    queryset = QuestionModel\
        .objects\
        .values('categories__title', 'categories__slug')\
        .annotate(Count('categories__title'))
    return queryset


def search_view(request):
    queryset = QuestionModel.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    context = {
        'title': 'Search',
        'queryset': queryset,
    }
    templates = 'Ecommunity/search_results.html'
    return render(request, templates, context)


def community_view(request, tag_slug=None, category_slug=None,):

    latest = NewsPost.objects.order_by('-time_stamp')[0:4]
    tag_count = get_tag_count()
    category_count = '00'
    Q_count = QuestionModel.objects.all().count()

    tag = None
    category = None

    queryset = QuestionModel.objects.order_by('-time_stamp')

    # latest = QuestionModel.objects.order_by('-time_stamp')[0:4]

    paginator = Paginator(queryset, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if category_slug:
        queryset = QuestionModel.objects.all()
        category = get_object_or_404(Categories, slug=category_slug)
        queryset = queryset.filter(categories=category)
        # paginator
        paginator = Paginator(queryset, 10)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = QuestionModel.objects.filter(tags__in=[tag])
        # paginator
        paginator = Paginator(queryset, 10)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

    context = {
        'tag': tag,
        'latest': latest,
        'Q_count': Q_count,
        'title': 'Community',
        'queryset': queryset,
        'tag_count': tag_count,
        'category_count': category_count,
        'page_request_var': page_request_var
    }
    templates = 'Ecommunity/community.html'
    return render(request, templates, context)


def rating(request, questionmodel_id):
    # objects.
    if request.method == 'POST':
        username = request.user.profile
        if request.POST.get('el_id'):
            ratings = Answers.objects.get(id=questionmodel_id)
            rate, created = Rate.objects.get_or_create(
                user=request.user, post_id=questionmodel_id)
            val = request.POST.get('val')

            int_ = int(val)
            print(int_)
            rate.rating = val
            rate.save()
            return JsonResponse({'success': 'true', 'score': int_}, safe=False)
    return HttpResponseRedirect(reverse('community:community'))


def post_view(request, questionmodel_id):

    latest = NewsPost.objects.order_by('-time_stamp')[0:4]

    tag_count = get_tag_count()
    category_count = get_category_count()

    # latest = QuestionModel.objects.order_by('-id')[0:4]

    post = get_object_or_404(
        QuestionModel, pk=questionmodel_id
    )
    test = post.get_answers.all()
    # test1 = post.get_answers.values('rates__rating')
    # print(test)
    # print(test1)
    post_tag_ids = QuestionModel.tags.values_list('id', flat=True)
    similar_post = QuestionModel.objects.filter(
        tags__in=post_tag_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-time_stamp')[:10]

    if request.user.is_authenticated:
        QuestionView.objects.get_or_create(user=request.user, post=post)
    form = AnswerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return HttpResponseRedirect(reverse("community:question", kwargs={
                'questionmodel_id': post.id
            }))

    if request.method == 'POST':
        username = request.user.profile
        if request.POST.get('post_id'):
            post_obj = QuestionModel.objects.get(id=questionmodel_id)

            if username in post_obj.liked.all():
                post_obj.liked.remove(username)
            else:
                post_obj.liked.add(username)

            like, created = Like.objects.get_or_create(
                user=request.user, post_id=questionmodel_id)

            if not created:
                if like.value == 'Like':
                    like.value == 'Unlike'
                else:
                    like.value == 'Like'

                like.save()
            data = {
                'value': like.value,
                'likes': post_obj.liked.all().count()
            }
            return JsonResponse(data, safe=False)

        return HttpResponseRedirect(reverse('community:question'))

    context = {
        "post": post,
        'form': form,
        'title': 'Post',
        'test': test,
        'latest': latest,
        'tag_count': tag_count,
        'similar_post': similar_post,
        'category_count': category_count,
    }
    templates = 'Ecommunity/post.html'
    return render(request, templates, context)


def like_post(request, questionmodel_id):
    user = request.user
    username = request.user.profile
    if request.method == 'POST':
        if request.POST.get('post_id'):
            # post_id = request.POST.get('post_id')
            post_obj = QuestionModel.objects.get(id=questionmodel_id)
            print(questionmodel_id)

            if username in post_obj.liked.all():
                post_obj.liked.remove(username)
            else:
                post_obj.liked.add(username)

            like, created = Like.objects.get_or_create(
                user=user, post_id=questionmodel_id)

            if not created:
                if like.value == 'Like':
                    like.value == 'Unlike'
                else:
                    like.value == 'Like'

            like.save()

    return HttpResponseRedirect(reverse(post_obj.get_absolute_url))


def support_view(request):
    return render(request, 'Ecommunity/support.html', {
        'title': 'Support'
    })


def refrencing_view(request):
    return render(request, 'Ecommunity/refrence.html', {
        'title': 'Refrence'
    })


# class PostLikeToggle(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         questionmodel_id = self.kwargs.get('questionmodel_id')
#         print(questionmodel_id)
#         obj = get_object_or_404(QuestionModel, pk=questionmodel_id)
#         url_ = obj.get_absolute_url()
#         user = self.request.user
#         username = self.request.user.profile

#         if user.is_authenticated:
#             print(user)
#             print(username)
#             if username in obj.liked.all():
#                 obj.liked.remove(username)
#             else:
#                 obj.liked.add(username)

#         return url_


# class PostLikeAPIToggle(APIView):
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, questionmodel_id, format=None):
#         # questionmodel_id = self.kwargs.get('questionmodel_id')
#         obj = get_object_or_404(QuestionModel, pk=questionmodel_id)
#         url_ = obj.get_absolute_url()
#         user = self.request.user
#         username = self.request.user.profile
#         updated = False
#         like = False
#         print(obj.liked.all().count())

#         if user.is_authenticated:
#             if username in obj.liked.all():
#                 like = False
#                 obj.liked.remove(username)
#             else:
#                 like = True
#                 obj.liked.add(username)

#             updated = True

#         data = {
#             'updated': updated,
#             'like': obj.liked.all().count()
#         }
#         # return url_
#         return Response(data)
