from django.conf import settings
from django.db import models
from django.shortcuts import reverse


class Bucket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=120)

    def get_absolute_url(self):
        return reverse('buckets:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
