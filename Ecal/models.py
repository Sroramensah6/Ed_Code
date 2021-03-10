from django.db import models
from django.utils import timezone


from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
