from django.test import TestCase
from django.shortcuts import reverse

from .models import Image, Tag, get_random_image_without_tags


class ImageModelTests(TestCase):
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

    def test_add_tags(self):
        """
        A user can add tags to an image
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
        on the new image to classify
        """
        image_a = Image.objects.get(file='img_a.jpeg')
        image_b = Image.objects.get(file='img_b.jpeg')

        bathroom = Tag.objects.get(name='bathroom')

        response = self.client.post(
            reverse('images:add_tags', args=(image_a.id,)),
            {'tags': bathroom.id},
            follow=True
        )

        self.assertRedirects(response, reverse('images:detail', args=(image_b.id, )))
