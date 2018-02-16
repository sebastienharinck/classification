import random

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Image(models.Model):
    file = models.ImageField()
    tags = models.ManyToManyField(Tag, blank=True)


def get_random_image_without_tags():
    ids = Image.objects.filter(tags=None).values_list('id', flat=True)
    if not ids:
        return False
    rand = random.choice(ids)
    return Image.objects.get(pk=rand)
