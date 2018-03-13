import random

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from buckets.models import *


class Image(models.Model):
    file = models.ImageField()
    bucket = models.ForeignKey(Bucket, on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse('images:detail', kwargs={'pk': self.pk})


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.DO_NOTHING)
    labels = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)


def get_all_images_ids_with_no_vote(bucket):
    q = Image.objects.filter(vote=None, bucket=bucket)
    q = q.values_list('id', flat=True)

    return q


def get_random_image_with_no_vote(bucket):
    ids = get_all_images_ids_with_no_vote(bucket)
    if not ids:
        return False
    rand = random.choice(ids)
    return Image.objects.get(pk=rand)
