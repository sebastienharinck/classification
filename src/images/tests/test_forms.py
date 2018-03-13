from django.test import TestCase
from django.contrib.auth.models import User

from images.forms import VoteForm
from buckets.models import Bucket, Label
from images.models import Image, Vote


class ImageFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        self.bucket = Bucket.objects.create(name='Bucket Name', user=self.user)
        self.image = Image.objects.create(file='img_a.jpg', bucket=self.bucket)
        self.label1 = Label.objects.create(name='Kitchen', bucket=self.bucket)
        self.label2 = Label.objects.create(name='Bathroom', bucket=self.bucket)

    #def test_vote_form(self):
    #    vote = Vote(pk=1, user=self.user, image=self.image, bucket=self.bucket)
    #    vote.labels.set([self.label1, self.label2])
    #    vote.save()
    #    form = VoteForm({
    #        'labels': self.label1,
    #    }, image=self.image, instance=vote)

    #    form.is_valid()
    #    print(form.errors)
    #    self.assertTrue(form.is_valid())
