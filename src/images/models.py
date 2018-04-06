import random
import os
import hashlib


from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


# todo : move in utils.py
def upload_to(instance, filename):
    instance.file.open()

    if not instance.hash:
        instance_hash = hashlib.sha512(instance.file.read())
        instance.hash = instance_hash.hexdigest()
        instance.file.seek(0)
    filename_base, filename_ext = os.path.splitext(filename)

    return "{0}{1}".format(instance.hash, filename_ext)


class Image(models.Model):
    file = models.ImageField(upload_to=upload_to, max_length=133)
    bucket = models.ForeignKey('buckets.Bucket', on_delete=models.DO_NOTHING)
    hash = models.CharField(max_length=128, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('images:detail', kwargs={'pk': self.pk})


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    label = models.ForeignKey('buckets.Label', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    choice = models.BooleanField()

    class Meta:
        ordering = ['-created_at']
