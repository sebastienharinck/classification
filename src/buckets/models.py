from django.conf import settings
from django.db import models
from django.shortcuts import reverse

from images.models import Image, Vote


class Bucket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=120)
    shared_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_users')

    def get_absolute_url(self):
        return reverse('buckets:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def get_all_votes(self):
        return Vote.objects.filter(image__bucket__pk=self.pk)

    def get_all_images_ids_with_no_vote(self):
        q = Image.objects.filter(vote=None, bucket=self)
        q = q.values_list('id', flat=True)

        return q

    def get_random_image_with_no_vote(self):
        ids = get_all_images_ids_with_no_vote(self)
        if not ids:
            return False
        rand = random.choice(ids)
        return Image.objects.get(pk=rand)


class Label(models.Model):
    name = models.CharField(max_length=120)
    bucket = models.ForeignKey(Bucket, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name
