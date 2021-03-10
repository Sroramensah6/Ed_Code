from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404


from .models import Comment
from.forms import CommentForm


def comment_thread(request, comment_id):
    # obj = get_object_or_404(Comment,  pk=comment_id)

    try:
        obj = Comment.objects.get(pk=comment_id)
    except:
        raise Http404

    post = obj.post
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
    context = {
        'comment': obj,
        'form': form,
    }
    template = 'ecomments/comment_thread.html'
    return render(request, template, context)


def comment_thread_delete(request, comment_id):
    # obj = get_object_or_404(Comment,  pk=comment_id)
    try:
        obj = Comment.objects.get(pk=comment_id)
    except:
        raise Http404

    if obj.user != request.user:
        response = HttpResponse(
            'What do you think, you\'re doing fam?.'
            'fuck off pussio boy '
        )
        response.status_code = 403
        return response
        # raise Http404

    post = obj.post
    if request.method == 'POST':
        parent_obj_url = obj.get_absolute_url()
        obj.delete()
        return HttpResponseRedirect(reverse("news:post-details", kwargs={
            'newspost_id': post.id
        }))
    context = {
        'object': obj,
    }
    template = 'ecomments/comfirm_delete.html'
    return render(request, template, context)
