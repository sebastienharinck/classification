from django.test import TestCase
from django.shortcuts import reverse

from .models import Image


class ImageModelTests(TestCase):
    def test_display_img(self):
        image = Image.objects.create(file='img.jpeg')
        response = self.client.get(reverse('images:detail', args=(image.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'img.jpeg')
