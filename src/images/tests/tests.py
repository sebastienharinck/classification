import os

from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.conf import settings

from images.models import *
from buckets.models import *

"""
class VoteTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        bucket = Bucket.objects.create(user=user, name='bucket test')
        file_img1 = os.path.join(settings.MEDIA_ROOT, 'img1.jpg')
        file_img2 = os.path.join(settings.MEDIA_ROOT, 'img2.jpg')
        Image.objects.create(file=file_img1, bucket=bucket)
        Image.objects.create(file=file_img2, bucket=bucket)
        Label.objects.create(name='kitchen', bucket=bucket)
        Label.objects.create(name='bathroom', bucket=bucket)
        Label.objects.create(name='bedroom', bucket=bucket)
        


    def test_a_user_cant_vote_without_login(self):

    image_a = Image.objects.get(pk=1)
    kitchen = Label.objects.get(name='kitchen')
    
    response = self.client.post(
        reverse('images:vote', args=(image_a.id,)),
        {'labels': (kitchen.id,)},
        follow=True
    )
    
    self.assertRedirects(response, '/accounts/login/?next=/images/1/vote/')
    
    def test_a_user_can_vote(self):

    image_a = Image.objects.get(pk=1)
    kitchen = Label.objects.get(name='kitchen')
    
    response = self.client.post(
        reverse('images:vote', args=(image_a.id,)),
        {'labels': (kitchen.id,)},
    )
    
    self.assertEqual(response.status_code, 302)


"""