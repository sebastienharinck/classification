from django.test import TestCase
from django.contrib.auth.models import User

from buckets.models import Bucket, Label
from images.models import *

from buckets.forms import get_all_images_ids_with_no_vote


class ImageModelTest(TestCase):

    def setUp(self):
        self.setUsers()
        self.setBuckets()
        self.setLabels()
        self.setImages()

    def setUsers(self):
        self.user_1 = User.objects.create_user(username='user1', email='user@example.com', password='userexample')
        self.user_2 = User.objects.create_user(username='user2', email='user2@example.com', password='userexample')

    def setBuckets(self):
        self.bucket_1 = Bucket.objects.create(name='my bucket', user=self.user_1)
        self.bucket_2 = Bucket.objects.create(name='my bucket 2', user=self.user_1)

    def setLabels(self):
        self.label_1 = Label.objects.create(name='Kitchen', bucket=self.bucket_1)
        self.label_2 = Label.objects.create(name='Bathroom', bucket=self.bucket_1)

    def setImages(self):
        self.image_1 = Image.objects.create(file='img1.jpg', bucket=self.bucket_1)
        self.image_2 = Image.objects.create(file='img2.jpg', bucket=self.bucket_1)
        self.image_3 = Image.objects.create(file='img3.jpg', bucket=self.bucket_1)
        self.image_4 = Image.objects.create(file='img4.jpg', bucket=self.bucket_2)

    def setVotes(self):
        Vote.objects.create(user=self.user_1, image=self.image_1, label=self.label_1, choice=True)
        Vote.objects.create(user=self.user_1, image=self.image_2, label=self.label_1, choice=False)
        Vote.objects.create(user=self.user_1, image=self.image_3, label=self.label_1, choice=False)

        Vote.objects.create(user=self.user_2, image=self.image_2, label=self.label_2, choice=True)
        Vote.objects.create(user=self.user_2, image=self.image_3, label=self.label_2, choice=False)

    def test_get_random_image_with_no_vote(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        Vote.objects.create(user=self.user_1, image=self.image_1, label=self.label_1, choice=True)

        random_image = get_all_images_ids_with_no_vote(label=self.label_1.id, user=self.user_1)

        self.assertEqual(list(random_image), [2, 3])

    def test_get_random_image_with_no_vote_other_label(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        Vote.objects.create(user=self.user_1, image=self.image_1, label=self.label_2, choice=True)

        random_image = get_all_images_ids_with_no_vote(label=self.label_1.id, user=self.user_1)

        self.assertEqual(list(random_image), [1, 2, 3])

    def test_get_random_image_with_no_vote_other_user(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        Vote.objects.create(user=self.user_1, image=self.image_1, label=self.label_1, choice=True)

        random_image = get_all_images_ids_with_no_vote(label=self.label_1.id, user=self.user_2)

        self.assertEqual(list(random_image), [1, 2, 3])

    def test_get_random_image_with_no_vote_other_user(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        self.setVotes()

        user1_label1_images = get_all_images_ids_with_no_vote(label=self.label_1.id, user=self.user_1)
        self.assertEqual(list(user1_label1_images), [])

        user1_label2_images = get_all_images_ids_with_no_vote(label=self.label_2.id, user=self.user_1)
        self.assertEqual(list(user1_label2_images), [1, 2, 3])

        user2_label1_images = get_all_images_ids_with_no_vote(label=self.label_1.id, user=self.user_2)
        self.assertEqual(list(user2_label1_images), [1, 2, 3])

        user2_label2_images = get_all_images_ids_with_no_vote(label=self.label_2.id, user=self.user_2)
        self.assertEqual(list(user2_label2_images), [1])



