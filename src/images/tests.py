from django.test import TestCase
from django.shortcuts import reverse

from .models import Image, Tag


class ImageModelTests(TestCase):
    def test_display_img(self):
        """
        A user can display an Image Model.
        """
        image = Image.objects.create(file='img.jpeg')
        response = self.client.get(reverse('images:detail', args=(image.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'img.jpeg')

    def test_add_tags(self):
        """
        A user can add tags to an image
        """
        image = Image.objects.create(file='img.jpeg')
        kitchen = Tag.objects.create(name='kitchen')
        bathroom = Tag.objects.create(name='bathroom')
        bedroom = Tag.objects.create(name='bedroom')

        self.client.post(
            reverse('images:add_tags', args=(image.id,)),
            {'tags': (kitchen.id, bedroom.id)}
        )

        expected_result = list(map(repr, [bedroom, kitchen]))
        self.assertQuerysetEqual(image.tags.order_by('name'), expected_result)
