from django.conf import settings
from django.db import models
from django.shortcuts import reverse


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=120)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk})
