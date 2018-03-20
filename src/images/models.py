import random
import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Image(models.Model):
    file = models.ImageField()
    bucket = models.ForeignKey('buckets.Bucket', on_delete=models.DO_NOTHING)
    hash = models.CharField(max_length=128, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('images:detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Image, self).save()
        if not self.hash:
            hash = hashlib.sha512(open(self.file.path, 'rb').read())
            self.hash = hash.hexdigest()
            super(Image, self).save()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    labels = models.ManyToManyField('buckets.Label')
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
