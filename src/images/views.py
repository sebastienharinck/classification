from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Image
from .forms import ImageForm


class DetailView(generic.DetailView):
    model = Image
    template_name = 'images/image.html'


def add_tags(request, pk):
    image = Image.objects.get(pk=pk)

    if request.method == 'POST':
        form = ImageForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/admin/')

    else:
        form = ImageForm()

    return render(request, 'images/add-tags.html', {'form': form, 'image': image})
