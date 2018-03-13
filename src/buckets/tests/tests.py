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

class CreateBucketTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='user@example.com', password='userexample')

    def test_bucket_user_create(self):
        """
        An identified user can create a bucket.
        """
        self.client.login(username='user', password='userexample')

        response = self.client.post(
            reverse('buckets:create'),
            {'name': 'bucket test'},
        )

        self.assertEqual(response.status_code, 302)
        bucket = Bucket.objects.get(pk=1)
        self.assertEqual(bucket.name, 'bucket test')
        self.assertEqual(bucket.user.id, 1)

    def test_bucket_user_create_redirect(self):
        """
        An identified user is redirect to the bucket list if he created a bucket.
        """
        self.client.login(username='user', password='userexample')

        response = self.client.post(
            reverse('buckets:create'),
            {'name': 'bucket test'},
            follow=True
        )

        self.assertRedirects(response, reverse('buckets:list'))

    def test_bucket_anonymous_create(self):
        """
        An anonymous user can't create a bucket.
        """
        response = self.client.post(
            reverse('buckets:create'),
            {'name': 'bucket test'},
            follow=True
        )

        self.assertRedirects(response, '/accounts/login/?next=/buckets/create/')

    def test_buckets_shared(self):
        """
        An identified user can access to the buckets shared with him.
        """
        pass


class LabelsBucketTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        Bucket.objects.create(name='bucket test', user=user)

    def test_add_labels_to_bucket(self):
        """
        A user can create labels in a bucket.
        """
        self.client.login(username='user', password='userexample')
        bucket = Bucket.objects.get(name='bucket test')

        response = self.client.post(
            reverse('buckets:add_labels', args=(bucket.id,)),
            {'name': 'test'}
        )

        self.assertEqual(response.status_code, 302)
        label = Label.objects.get(pk=1)
        self.assertEqual(label.name, 'test')
        self.assertEqual(label.bucket.name, 'bucket test')

    def test_add_labels_to_bucket_redirect(self):
        """
        A user is redirect to the bucket view after adding labels.
        """
        self.client.login(username='user', password='userexample')
        bucket = Bucket.objects.get(name='bucket test')

        response = self.client.post(
            reverse('buckets:add_labels', args=(bucket.id,)),
            {'name': 'test'},
            follow=True
        )

        self.assertRedirects(response, reverse('buckets:detail', args=(bucket.id,)))

    def test_add_labels_to_bucket_denied(self):
        """
        A anonymous user can't add labels to another bucket.
        """
        bucket = Bucket.objects.get(name='bucket test')

        response = self.client.post(
            reverse('buckets:add_labels', args=(bucket.id,)),
            {'name': 'test'},
            follow=True
        )

        self.assertRedirects(response, '/accounts/login/?next=/buckets/1/add-labels/')

    def test_add_labels_to_another_bucket_denied(self):
        """
        A user can't add labels to another bucket.
        """
        User.objects.create_user(username='eviluser', email='user@example.com', password='userexample')
        self.client.login(username='eviluser', password='userexample')
        bucket = Bucket.objects.get(name='bucket test')

        response = self.client.post(
            reverse('buckets:add_labels', args=(bucket.id,)),
            {'name': 'test'}
        )

        self.assertEqual(response.status_code, 403)


class ImagesBucketViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        Bucket.objects.create(name='Kitchen', user=user)

    def test_user_can_add_images_to_bucket(self):
        """
        A user can add images to a bucket.
        """
        self.client.login(username='user', password='userexample')
        bucket = Bucket.objects.get(name='Kitchen')

        f1 = open(os.path.join(os.path.dirname(__file__), "images/kitchen-3215407_640.jpg"), "rb")
        f2 = open(os.path.join(os.path.dirname(__file__), "images/modern-kitchen-3217932_640.jpg"), "rb")

        response = self.client.post(
            reverse('buckets:add_images', args=(bucket.id,)),
            {'files': [f1, f2]},
        )

        f1.close()
        f2.close()

        self.assertEqual(response.status_code, 302)
        image1 = Image.objects.get(pk=1)
        image2 = Image.objects.get(pk=2)
        self.assertIn('kitchen-3215407_640', image1.file.url)
        self.assertIn('modern-kitchen-3217932_640', image2.file.url)
        self.assertEqual(image1.bucket.id, 1)
        self.assertEqual(image2.bucket.id, 1)


class DetailBucketViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        bucket = Bucket.objects.create(name='Kitchen', user=user)
        Label.objects.create(name='table', bucket=bucket)

    def test_user_can_access_to_the_add_labels_page_from_bucket_view(self):
        """
        A user can access to the "add_labels" page from the bucket detail.
        """
        self.client.login(username='user', password='userexample')
        bucket = Bucket.objects.get(name='Kitchen')

        response = self.client.get(reverse('buckets:detail', args=(bucket.id,)))

        self.assertContains(response, reverse('buckets:add_labels', args=(bucket.id,)))

    def test_user_can_see_the_labels_on_the_bucket_view(self):
        """
        A user can see his labels on the bucket view.
        """
        self.client.login(username='user', password='userexample')
        bucket = Bucket.objects.get(name='Kitchen')

        response = self.client.get(reverse('buckets:detail', args=(bucket.id,)))

        self.assertContains(response, 'table')
