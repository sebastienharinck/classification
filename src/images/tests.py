from django.test import TestCase
from django.shortcuts import reverse

from .models import Image, Tag


class ImageTests(TestCase):
    def setUp(self):
        Image.objects.create(file='img_a.jpeg')
        Image.objects.create(file='img_b.jpeg')
        Tag.objects.create(name='kitchen')
        Tag.objects.create(name='bathroom')
        Tag.objects.create(name='bedroom')

    def test_homepage(self):
        """
        A user can display the homepage.
        """
        response = self.client.get(reverse('images:home'))
        self.assertContains(response, 'Welcome')

    def test_homepage_start_classification(self):
        """
        If there still have no tagged images, a user can start a classification.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')

        response = self.client.get(reverse('images:home'))
        self.assertIn('next_img', response.context)
        self.assertIn(response.context['next_img'], [image_a.id, image_b.id])

    def test_homepage_all_images_are_tagged(self):
        """
        If all images are tagged, a user must see a message and can't start a classification.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')

        bedroom = Tag.objects.get(name='bedroom')

        self.client.post(
            reverse('images:add_tags', args=(image_a.id,)),
            {'tags': bedroom.id}
        )

        self.client.post(
            reverse('images:add_tags', args=(image_b.id,)),
            {'tags': bedroom.id},
            follow=True
        )

        response = self.client.get(reverse('images:home'))
        self.assertNotIn('next_img', response.context)
        self.assertContains(response, "It seems that all images are tagged")

    def test_display_img(self):
        """
        A user can display an Image Model.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        response = self.client.get(reverse('images:detail', args=(image_a.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'img_a.jpeg')

    def test_add_tags(self):
        """
        A user can add tags to an image.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        kitchen = Tag.objects.get(name='kitchen')
        bedroom = Tag.objects.get(name='bedroom')

        self.client.post(
            reverse('images:add_tags', args=(image_a.id,)),
            {'tags': (kitchen.id, bedroom.id)}
        )

        expected_result = list(map(repr, [bedroom, kitchen]))
        self.assertQuerysetEqual(image_a.tags.order_by('name'), expected_result)

    def test_random_redirection(self):
        """
        When a user add tags to an image, he must to be redirected
        on the new image to classify.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')

        bathroom = Tag.objects.get(name='bathroom')

        response = self.client.post(
            reverse('images:add_tags', args=(image_a.id,)),
            {'tags': bathroom.id},
            follow=True
        )

        self.assertRedirects(response, reverse('images:add_tags', args=(image_b.id, )))

    def test_all_images_are_tagged(self):
        """
        When all images are tagged, the user is redirect to the congratulations page.
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')

        bathroom = Tag.objects.get(name='bathroom')

        self.client.post(
            reverse('images:add_tags', args=(image_a.id,)),
            {'tags': bathroom.id}
        )

        response = self.client.post(
            reverse('images:add_tags', args=(image_b.id,)),
            {'tags': bathroom.id},
            follow=True
        )

        self.assertRedirects(response, reverse('images:congratulations'))
