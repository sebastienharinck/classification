import random

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse


class Tag(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Image(models.Model):
    file = models.ImageField()


class Bucket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=120)

    def get_absolute_url(self):
        return reverse('images:bucket_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)


def get_all_images_ids_with_no_vote():
    q = Image.objects.filter(vote=None)
    q = q.values_list('id', flat=True)

    return q


def get_random_image_with_no_vote():
    ids = get_all_images_ids_with_no_vote()
    if not ids:
        return False
    rand = random.choice(ids)
    return Image.objects.get(pk=rand)
