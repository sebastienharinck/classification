from django.test import TestCase
from django.shortcuts import reverse

from django.contrib.auth.models import User
from buckets.models import Bucket, Label


class VoteByLabelsCreateViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        self.bucket = Bucket.objects.create(name='bucket test', user=user)
        self.label = Label.objects.create(name='table', bucket=self.bucket)

    def test_a_user_can_display_8_random_images_from_bucket(self):
        """
        A user can display 8 random images from a bucket with not vote
        """
        response = self.client.get(reverse('buckets:vote_by_labels', args=(self.bucket.id, self.label.id,)))


