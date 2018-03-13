import os

from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from buckets.models import *
from images.models import Image


class BucketModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='user@example.com', password='userexample')

    def test_string_representation(self):
        user = User.objects.get(pk=1)
        bucket = Bucket.objects.create(user=user, name='My test Bucket')
        self.assertEqual(str(bucket), bucket.name)


class LabelModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        Bucket.objects.create(user=user, name='My test Bucket')

    def test_label_string_representation(self):
        bucket = Bucket.objects.get(pk=1)
        label = Label.objects.create(bucket=bucket, name='My custom Label')
        self.assertEqual(str(label), label.name)
