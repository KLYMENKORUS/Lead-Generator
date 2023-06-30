from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    keyword = models.CharField(max_length=255, verbose_name='Keyword',
                               blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name='Location',
                                blank=True, null=True)
