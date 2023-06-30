from django.contrib.auth.models import User
from django.db import models


class Lead(models.Model):
    name = models.CharField(max_length=255, verbose_name='Lead name', unique=True)
    address = models.CharField(max_length=1028, verbose_name='Address')
    phone_number = models.CharField(max_length=16, verbose_name='Phone number', blank=True, null=True)
    url = models.URLField(verbose_name='URL', blank=True, null=True)
    keyword = models.CharField(max_length=255, verbose_name='Keyword',
                               blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name='Location',
                                blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']

