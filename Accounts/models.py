from django.db import models
from django.utils import timezone


from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(
        default='/Profile_pc/avatar-1577909_1280.png', upload_to='Profile_pc', null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=30, blank=True)
    signup_confirmation = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
