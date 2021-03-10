from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from News.models import NewsPost
from Accounts.models import Profile


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        qs = super(CommentManager, self).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        NewsPost, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Leave a Comment')
    time_reply = models.TimeField(auto_now_add=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-time_stamp']

    def get_absolute_url(self):
        return reverse("comment:thread", kwargs={
            'comment_id': self.id
        })

    def __str__(self):
        return self.user.username

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
