from django.test import TestCase
from django.contrib.auth.models import User

from buckets.models import Bucket, Label
from projects.models import Project


class BucketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        self.superuser = User.objects.create_superuser(username='superuser', email='superuser@example.com', password='superuserexample')

        self.project = Project.objects.create(user=self.user, name='Project', description='my project')

        self.bucket = Bucket.objects.create(name='Bucket', user=self.user, project=self.project)
        self.superuser_bucket = Bucket.objects.create(name='Super Bucket', user=self.superuser, project=self.project)

    def test_string_representation(self):
        user = User.objects.get(pk=1)
        bucket = Bucket.objects.create(user=user, name='My test Bucket', project=self.project)
        self.assertEqual(str(bucket), bucket.name)

    def test_can_delete_a_bucket(self):
        self.bucket.delete()
        self.assertEqual(Bucket.objects.filter(name='Bucket').count(), 0)

    def test_can_delete_superuser_bucket(self):
        self.superuser_bucket.delete()
        self.assertEqual(Bucket.objects.filter(name='Super Bucket').count(), 0)


class LabelModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        self.project = Project.objects.create(user=self.user, name='Project', description='my project')
        Bucket.objects.create(user=self.user, name='My test Bucket', project=self.project)

    def test_label_string_representation(self):
        bucket = Bucket.objects.get(pk=1)
        label = Label.objects.create(bucket=bucket, name='My custom Label', project=self.project)
        self.assertEqual(str(label), label.name)
