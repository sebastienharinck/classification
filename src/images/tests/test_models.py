import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

from buckets.models import Bucket, Label
from images.models import *


class ImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        self.bucket = Bucket.objects.create(name='my bucket', user=self.user)
        self.label_1 = Label.objects.create(name='Kitchen', bucket=self.bucket)
        self.label_2 = Label.objects.create(name='Bathroom', bucket=self.bucket)

    def test_save(self):
        """
        When a image is create a hash of the img needs to be compute
        """

        image_file = os.path.join(settings.MEDIA_ROOT, 'img1.jpg')
        image = Image.objects.create(file=image_file, bucket=self.bucket)
        self.assertEqual(image.hash, 'ec86cff8c9fab38b601df2fd579aacd3c788c4d18d0d9f7f243b4ab02f09dd60312672accdde90f08209665031cf248fb2a7b785c4bb2d267a0ffdeae4fa0c06')

    def test_get_absolute_url(self):
        image = Image.objects.create(file='img1.jpg', bucket=self.bucket)
        self.assertEqual(image.get_absolute_url(), '/images/1/')

    def test_get_random_image_with_no_vote(self):
        image1 = Image.objects.create(file='img1.jpg', bucket=self.bucket)
        image2 = Image.objects.create(file='img2.jpg', bucket=self.bucket)
        image3 = Image.objects.create(file='img3.jpg', bucket=self.bucket)
        vote1 = Vote.objects.create(user=self.user, image=image1)
        vote1.labels.set([self.label_1, self.label_2])
        vote2 = Vote.objects.create(user=self.user, image=image2)
        vote2.labels.set([self.label_1])

        random_image = get_random_image_with_no_vote(self.bucket)
        self.assertEqual(random_image.id, image3.id)
