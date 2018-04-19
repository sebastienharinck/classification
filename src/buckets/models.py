from django.conf import settings
from django.db import models
from django.shortcuts import reverse

from projects.models import Project


class Label(models.Model):
    name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Bucket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    shared_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_users', blank=True)
    labels = models.ManyToManyField(Label)

    def get_absolute_url(self):
        return reverse('buckets:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        super(Bucket, self).delete(using=None, keep_parents=False)
