from django.views import generic

from .models import Image


class DetailView(generic.DetailView):
    model = Image
    template_name = 'images/image.html'
