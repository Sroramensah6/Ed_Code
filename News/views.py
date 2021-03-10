from urllib.parse import quote_plus
from django.urls import reverse
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taggit.models import Tag

from .models import NewsPost, PostView, Categories, LikePost

from Accounts.models import Profile

from Marketing.models import Subscriber

from Ecomments.models import Comment
from Ecomments.forms import CommentForm

from .forms import PostForm


def get_author(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search_view(request):
    queryset = NewsPost.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(over_view__icontains=query)
        ).distinct()

    context = {
        'title': 'Search',
        'queryset': queryset,
    }
    templates = 'Enews/search_results.html'
    return render(request, templates, context)


def get_category_count():
    queryset = NewsPost\
        .objects\
        .values('categories__title', 'categories__slug')\
        .annotate(Count('categories__title'))
    return queryset


def nav(request):
    return render(request, 'Enews/nav.html')


def news_view(request):
    # profile = request.user.profile
    featured = NewsPost.objects.all()[0:3]
    # .order_by('-time_stamp')[0:3]
    latest = NewsPost.objects.filter(
        publish__lte=timezone.now()).order_by('-time_stamp')[:5]
    if request.method == "POST":
        if request.POST.get("email"):
            subscriber = Subscriber()
            subscriber.email = request.POST.get("email")
            subscriber.save()
    context = {
        'title': 'News',
        'object_list': featured,
        'latest': latest
    }
    templates = 'Enews/index.html'
    return render(request, templates, context)


def blog_view(request, category_slug=None, tag_slug=None):

    category = None
    category_count = get_category_count()
    # cat = Categories.objects.all().annotate()
    queryset = NewsPost.objects.active()
    categories_title = NewsPost.objects.values('categories__title')
    # page request variable
    paginator = Paginator(queryset, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    tag = None
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    latest = NewsPost.objects.filter(
        publish__lte=timezone.now()).order_by('-time_stamp')[:5]
    # if category_slug_post:
    #     pass
    if category_slug:
        queryset = NewsPost.objects.all()
        category = get_object_or_404(Categories, slug=category_slug)
        queryset = queryset.filter(categories=category)
        # paginator
        paginator = Paginator(queryset, 4)
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
        queryset = NewsPost.objects.filter(tags__in=[tag])
        # paginator
        paginator = Paginator(queryset, 1)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

    context = {
        'title': 'Blog',
        'latest': latest,
        # 'tag': categories_title,
        # 'categorie': categorie,
        'category': category,
        'queryset': queryset,
        'category_count': category_count,
        'page_request_var': page_request_var
    }
    templates = 'Enews/blog.html'

    return render(request, templates, context)


def post_view(request, newspost_id):
    post = get_object_or_404(
        NewsPost, pk=newspost_id
    )
    print(post.author.user.username)
    print(request.user)
    # if post.featured:
    #     if request.user != post.author.user.username:
    #         raise Http404
    category_count = get_category_count()
    latest = NewsPost.objects.filter(
        publish__lte=timezone.now()).order_by('-time_stamp')[:5]

    share_string = quote_plus(post.title)
    post_tags_id = NewsPost.tags.values_list('id', flat=True)
    postes = NewsPost.objects.values_list('categories', flat=True, )
    similar_post = NewsPost.objects.filter(
        categories__in=postes).exclude(pk=post.id)
    similar_post = similar_post.annotate(same_tags=Count(
        'categories')).order_by('-same_tags', '-time_stamp')[:3]
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            blog_post = post
            content = form.cleaned_data.get('content')
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs[0]  # first()
            new_comment, created = Comment.objects.get_or_create(
                user=user,
                post=blog_post,
                content=content,
                parent=parent_obj
            )
            return HttpResponseRedirect(reverse("news:post-details", kwargs={
                'newspost_id': post.id
            }))

    if request.method == 'POST':
        username = request.user.profile
        if request.POST.get('post_id'):
            post = NewsPost.objects.get(id=newspost_id)

            if username in post.liked.all():
                post.liked.remove(username)
            else:
                post.liked.add(username)

            like, created = LikePost.objects.get_or_create(
                user=request.user, post_id=newspost_id)

            if not created:
                if like.value == 'Like':
                    like.value == 'Unlike'
                else:
                    like.value == 'Like'

                like.save()

            data = {
                'value': like.value,
                'likes': post.liked.all().count()
            }

            return JsonResponse(data, safe=False)

        return HttpResponseRedirect(reverse(post.get_absolute_url()))

    context = {
        "post": post,
        'form': form,
        'title': 'Post',
        'latest': latest,
        'share_string': share_string,
        'similar_post': similar_post,
        'category_count': category_count,
    }

    templates = 'Enews/post_view.html'

    return render(request, templates, context)


def post_create_view(request):
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.instance.featured = True
            form.save()
            return HttpResponseRedirect(reverse("news:post-details", kwargs={
                'newspost_id': form.instance.id
            }))
    context = {
        'form': form,
        'title': 'Create a post',
    }
    templates = 'Enews/post_create.html'
    return render(request, templates, context)


def post_update_view(request, newspost_id):

    update_results = get_object_or_404(
        NewsPost, pk=newspost_id
    )
    form = PostForm(request.POST or None, request.FILES or None,
                    instance=update_results)
    author = get_author(request.user)
    if(request.method == "POST"):
        if form.is_valid():
            form.instance.author = author
            form.save()
            return HttpResponseRedirect(reverse("news:post-details", kwargs={
                'newspost_id': form.instance.id
            }))
    context = {
        'form': form,
        'title': 'Update',
    }
    templates = 'Enews/post_create.html'
    return render(request, templates, context)


def post_delete_view(request, newspost_id):

    delete_results = get_object_or_404(
        NewsPost, pk=newspost_id
    )

    delete_results.delete()

    return HttpResponseRedirect(reverse("news:blog"))


# post_view
    # nice = postes.categories.values_list('id', flat=True)
    # post_categories_slug = {poll.categories.values_list(
    #     'id', flat=True) for poll in postes}
    # for poll in postes:
    #     choice_1 = poll.categories.all()
    #     print(choice_1)
    # postes = NewsPost\
    #     .objects\
    #     .values('categories__title', 'categories__slug')

    # similar_post = NewsPost.objects.values('title').annotate(
    #     Count('categories__title')).order_by('-time_stamp')[:1]
    # similar_post = NewsPost.objects.filter(categories__in=post_categories_slug).exclude(pk=post.id)
