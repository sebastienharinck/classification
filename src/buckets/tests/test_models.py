import os

from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from buckets.models import *
from images.models import Image


class TestsListBuckets(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        Bucket.objects.create(user=user, name='bucket start')

    def test_buckets_anonymous(self):
        """
        An anonymous user can't display the buckets page.
        """
        response = self.client.get(reverse('buckets:list'))
        self.assertRedirects(response, '/accounts/login/?next=/buckets/')

    def test_buckets_connected(self):
        """
        An identified user can display the buckets page.
        """
        self.client.login(username='user', password='userexample')

        response = self.client.get(reverse('buckets:list'))
        self.assertEqual(response.status_code, 200)

    def test_buckets_empty(self):
        """
        If the identified user have no bucket, a message is displaying to encourage him to create one.
        """
        User.objects.create_user(username='empty', email='user@example.com', password='userexample')
        self.client.login(username='empty', password='userexample')

        response = self.client.get(reverse('buckets:list'))
        self.assertContains(response, 'No bucket yet.')

    def test_buckets_access_authorized(self):
        """
        An identified user can only access to his buckets.
        """
        self.client.login(username='user', password='userexample')

        response = self.client.get(reverse('buckets:list'))
        self.assertContains(response, 'bucket start')

    def test_bucket_access_denied(self):
        """
        An identified user can't display the buckets of another user.
        """
        User.objects.create_user(username='eviluser', email='user@example.com', password='userexample')
        self.client.login(username='eviluser', password='userexample')

        response = self.client.get(reverse('buckets:list'))
        self.assertNotContains(response, 'bucket start')

    def test_buckets_create_bucket(self):
        """
        A user can access to the page to create a bucket.
        """
        self.client.login(username='user', password='userexample')

        response = self.client.get(reverse('buckets:list'))
        self.assertContains(response, reverse('buckets:create'))