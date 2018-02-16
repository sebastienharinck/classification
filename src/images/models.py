import random

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Image(models.Model):
    file = models.ImageField()
    tags = models.ManyToManyField(Tag, blank=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)


def get_random_image_without_tags():
    ids = Image.objects.filter(tags=None).values_list('id', flat=True)
    if not ids:
        return False
    rand = random.choice(ids)
    return Image.objects.get(pk=rand)
