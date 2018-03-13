from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import *
from buckets.models import *


class VoteTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        bucket = Bucket.objects.create(user=user, name='bucket test')
        Image.objects.create(file='img_a.jpeg', bucket=bucket)
        Image.objects.create(file='img_b.jpeg', bucket=bucket)
        Label.objects.create(name='kitchen', bucket=bucket)
        Label.objects.create(name='bathroom', bucket=bucket)
        Label.objects.create(name='bedroom', bucket=bucket)

    def test_a_user_cant_vote_without_login(self):
        """
        A user can't vote if he is not authenticated.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        kitchen = Label.objects.get(name='kitchen')

        response = self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'labels': (kitchen.id,)},
            follow=True
        )

        self.assertRedirects(response, '/accounts/login/?next=/images/1/vote/')

    def test_a_user_can_vote(self):
        """
        A user can vote on the image with only the tags of the bucket.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        kitchen = Label.objects.get(name='kitchen')

        response = self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'labels': (kitchen.id,)},
        )

        self.assertEqual(response.status_code, 302)
