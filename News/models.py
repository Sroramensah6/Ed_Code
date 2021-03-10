from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django_userforeignkey.models.fields import UserForeignKey

from markdown_deux import markdown
from taggit.managers import TaggableManager

from .util import get_read_time, words_count

from tinymce import HTMLField
from Accounts.models import Profile
# from Ecomments.models import Comment


class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).filter(featured=True).filter(publish__lte=timezone.now())


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('NewsPost', on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username


LIKE_CHOICES = (
    ('like', 'Like'),
    ('unlike', 'unLike'),
)


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'NewsPost', related_name='likes', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='like', max_length=10)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.post)


class Categories(models.Model):
    title = models.CharField(verbose_name='title', max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-title',)

    def __str__(self):
        return self.title

    def get_cat_url(self):
        return reverse("news:post-category", args=[self.slug])


class NewsPost(models.Model):
    # user = UserForeignKey(
    #     auto_user_add=True, on_delete=models.CASCADE)
    author = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='title', max_length=100)
    over_view = models.TextField(blank=True, null=True)
    content = models.TextField(verbose_name='')
    tags = TaggableManager()
    comment_count = models.IntegerField(default=0)
    thumbnail = models.ImageField(
        default='/News_Pictures/element5-digital-WCPg9ROZbM0-unsplash.jpg', upload_to='News_Pictures', null=True, blank=True)
    # categories = models.ManyToManyField(Category)
    categories = models.ManyToManyField(Categories)
    featured = models.BooleanField(default=True)
    previous_post = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='previous', null=True, blank=True)
    next_post = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='next', null=True, blank=True)
    liked = models.ManyToManyField(
        Profile, related_name='like', default=None, blank=True)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    words_count = models.IntegerField(default=0)
    read_time = models.TimeField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:post-details", kwargs={
            'newspost_id': self.id
        })

    def get_over_view_mark_down(self):
        over_view = self.over_view
        markdown_text = markdown(over_view)
        return mark_safe(markdown_text)

    def get_mark_down(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_tag_url(self):
        return reverse("news:post-by-tag", kwargs={
            'newspost_id': self.id
        })

    def get_like_url(self):
        return reverse("news:like", kwargs={
            'newspost_id': self.id
        })

    def get_update_url(self):
        return reverse("news:update-post", kwargs={
            'newspost_id': self.id
        })

    def get_delete_url(self):
        return reverse("news:delete-post", kwargs={
            'newspost_id': self.id
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-time_stamp')

    @property
    def num_liked(self):
        return self.liked.all().count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    # @property
    # def comment_count(self):
    #     return Comment.objects.filter(post=self).count()


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        html_string = instance.content
        markdown_text = markdown(html_string)
        read_time_var = get_read_time(markdown_text)
        words_count_var = words_count(markdown_text)
        instance.read_time = read_time_var
        instance.words_count = words_count_var


pre_save.connect(pre_save_post_receiver, sender=NewsPost)
