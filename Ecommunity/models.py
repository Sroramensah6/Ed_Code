from django.db import models
from django.urls import reverse
from django.db.models import Count
from Accounts.models import Profile
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from taggit.managers import TaggableManager
from tinymce import HTMLField


class QuestionView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('QuestionModel', on_delete=models.CASCADE)
    # time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # class Meta:
    #     ordering = ['time_stamp']

    def __str__(self):
        return self.user.username


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Answers', related_name='rates', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0),
    ])
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

 
class Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = HTMLField()
    rating = models.ManyToManyField(
        Profile, related_name='rate', default=None, blank=True)
    post = models.ForeignKey(
        'QuestionModel', related_name='answers', on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def get_rate_url(self):
        return reverse("community:rate", kwargs={
            'questionmodel_id': self.id
        })

    @property
    def rate_count(self):
        return Rate.objects.filter(post=self).count()

    @property
    def get_rating(self):
        return self.rates.all().order_by('-time_stamp')


class Categories(models.Model):
    title = models.CharField(verbose_name='title', max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_cat_url(self):
        return reverse("community:category", args=[self.slug])


LIKE_CHOICES = (
    ('like', 'Like'),
    ('unlike', 'unLike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'QuestionModel', related_name='likes', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='like', max_length=10)
    # time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.post)


class QuestionModel(models.Model):
    author = models.ForeignKey(
        Profile, related_name='author', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='title', max_length=100)
    content = HTMLField()
    tags = TaggableManager()
    categories = models.ManyToManyField(Categories)
    liked = models.ManyToManyField(
        Profile, related_name='liked', default=None, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("community:question", kwargs={
            'questionmodel_id': self.id
        })

    def get_like_url(self):
        return reverse("community:like", kwargs={
            'questionmodel_id': self.id
        })

    def get_api_like_url(self):
        return reverse("community:like-api", kwargs={
            'questionmodel_id': self.id
        })

    @property
    def num_liked(self):
        return self.liked.all().count()

    @property
    def view_count(self):
        return QuestionView.objects.filter(post=self).count()

    @property
    def answers_count(self):
        return Answers.objects.filter(post=self).count()

    @property
    def get_answers(self):
        return self.answers.all().order_by('-time_stamp')
