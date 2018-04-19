import hashlib
import random

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .utils import upload_to

from buckets.models import *


class ImageManager(models.Manager):
    @staticmethod
    def get_all_ids_with_no_vote(bucket, label, user=None):
        """
        @todo : improve the request
        """
        label = Label.objects.get(pk=label)

        hashes = Image.objects.filter(vote__in=Vote.objects.filter(label=label, user=user)).values_list('hash', flat=True)
        q = Image.objects.filter(~Q(hash__in=hashes), bucket=bucket)
        q = q.values_list('id', flat=True)

        return q

    @staticmethod
    def get_random_with_no_vote(bucket):
        ids = ImageManager.get_all_ids_with_no_vote(bucket)
        if not ids:
            return False
        rand = random.choice(ids)
        return Image.objects.filter(pk=rand)

    @staticmethod
    def get_samples_with_no_vote(bucket, label, number, user=None):
        ids = ImageManager.get_all_ids_with_no_vote(bucket, label, user)
        if not ids:
            return []
        ids_size = len(ids)
        if ids_size > number:
            rand = random.sample(list(ids), number)
        else:
            rand = random.sample(list(ids), ids_size)
        return Image.objects.filter(id__in=rand)


class Image(models.Model):
    file = models.ImageField(upload_to=upload_to, max_length=133)
    bucket = models.ForeignKey('buckets.Bucket', on_delete=models.CASCADE)
    hash = models.CharField(max_length=128, blank=True, null=True)

    objects = ImageManager()

    def __str__(self):
        return str(self.hash)

    def get_absolute_url(self):
        return reverse('images:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = hashlib.sha256(self.file.read()).hexdigest()
        if not Image.objects.filter(hash=self.hash, bucket=self.bucket).exists():
            super().save(*args, **kwargs)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    label = models.ForeignKey('buckets.Label', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    choice = models.BooleanField()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not Vote.objects.filter(user=self.user, image=self.image, label=self.label).exists():
            super().save(*args, **kwargs)
