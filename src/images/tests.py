from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import *


class ImageTests(TestCase):
    def setUp(self):
        Image.objects.create(file='img_a.jpeg')
        Image.objects.create(file='img_b.jpeg')
        Tag.objects.create(name='kitchen')
        Tag.objects.create(name='bathroom')
        Tag.objects.create(name='bedroom')

    def test_display_img(self):
        """
        A user can display an Image Model.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        response = self.client.get(reverse('images:detail', args=(image_a.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'img_a.jpeg')


class HomeTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@example.com', password='userexample')
        image_a = Image.objects.create(file='img_a.jpeg')
        kitchen = Tag.objects.create(name='kitchen')
        vote = Vote.objects.create(user=user, image=image_a)
        vote.tags.add(kitchen)

    def test_homepage(self):
        """
        A user can display the homepage.
        """
        response = self.client.get(reverse('images:home'))
        self.assertContains(response, 'Welcome')

    def test_homepage_all_images_are_tagged(self):
        """
        If all images are tagged, the user see a message on the homepage.
        """
        response = self.client.get(reverse('images:home'))
        self.assertContains(response, 'It seems that all images are tagged.')

    def test_homepage_start_classification(self):
        """
        If there still have no tagged images, a user can start a classification.
        """
        image_b = Image.objects.create(file='img_b.jpeg')

        response = self.client.get(reverse('images:home'))
        self.assertIn('next_img', response.context)
        self.assertEqual(response.context['next_img'], image_b.id)


class VoteTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='user@example.com', password='userexample')
        Image.objects.create(file='img_a.jpeg')
        Image.objects.create(file='img_b.jpeg')
        Tag.objects.create(name='kitchen')
        Tag.objects.create(name='bathroom')
        Tag.objects.create(name='bedroom')

    def test_a_user_cant_vote_without_login(self):
        """
        A user can't vote if he is not authenticated.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        kitchen = Tag.objects.get(name='kitchen')

        response = self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'tags': (kitchen.id, kitchen.id)},
            follow=True
        )

        self.assertRedirects(response, '/accounts/login/?next=/images/1/vote/')

    def test_a_user_can_vote(self):
        """
        If all images are not tagged or the user didn't tagged all images, and if the user is logged,
        the user can vote on the image.
        """
        self.client.login(username='user', password='userexample')

        image_a = Image.objects.get(file='img_a.jpeg')
        kitchen = Tag.objects.get(name='kitchen')

        response = self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'tags': (kitchen.id, kitchen.id)},
        )

        self.assertEqual(response.status_code, 302)
        vote = Vote.objects.get(pk=1)
        expected_result = list(map(repr, [kitchen]))
        self.assertQuerysetEqual(vote.tags.all(), expected_result)

    def test_random_redirection(self):
        """
        When a user vote on an image, he must to be redirected
        on the new image to vote.
        """
        self.client.login(username='user', password='userexample')

        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')
        kitchen = Tag.objects.get(name='kitchen')

        response = self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'tags': (kitchen.id, kitchen.id)},
            follow=True,
        )

        self.assertRedirects(response, reverse('images:vote', args=(image_b.id, )))

    def test_a_user_cant_vote_twice_on_the_same_image(self):
        """
        A User can't vote twice on the same image.
        """
        pass

    def test_all_images_are_tagged(self):
        """
        If all images are tagged, the user can't vote and see a message
        tell him that all images are tagged.
        """
        self.client.login(username='user', password='userexample')

        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')
        kitchen = Tag.objects.get(name='kitchen')

        self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'tags': (kitchen.id, kitchen.id)},
            follow=True,
        )

        response = self.client.post(
            reverse('images:vote', args=(image_b.id,)),
            {'tags': (kitchen.id)},
            follow=True,
        )

        self.assertRedirects(response, reverse('images:congratulations'))

    def test_get_images_with_no_vote(self):
        """
        We must to be able to find all the images that have no vote.
        """
        self.client.login(username='user', password='userexample')

        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')
        image_c = Image.objects.create(file='img_c.jpeg')
        kitchen = Tag.objects.get(name='kitchen')

        self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'tags': (kitchen.id, kitchen.id)},
            follow=True,
        )

        img_ids = get_all_images_ids_with_no_vote()
        expected_result = list(map(repr, [image_b.id, image_c.id]))
        self.assertQuerysetEqual(img_ids.order_by('id'), expected_result)

    def test_get_random_image_with_no_vote(self):
        """
        We must to be able to get a random image that is not tagged.
        """
        self.client.login(username='user', password='userexample')

        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')
        kitchen = Tag.objects.get(name='kitchen')

        self.client.post(
            reverse('images:vote', args=(image_a.id,)),
            {'tags': (kitchen.id, kitchen.id)},
            follow=True,
        )

        img_random = get_random_image_with_no_vote()
        self.assertEqual(img_random.id, image_b.id)







