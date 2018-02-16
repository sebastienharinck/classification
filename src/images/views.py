from django.views.generic import DetailView, TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .forms import ImageForm
from .models import Image, get_random_image_without_tags


class DetailView(DetailView):
    model = Image
    template_name = 'images/image.html'

class CongratulationsView(TemplateView):
    template_name = 'images/congratulations.html'


def add_tags(request, pk):
    image = Image.objects.get(pk=pk)

    if request.method == 'POST':
        form = ImageForm(request.POST, instance=image)

        if form.is_valid():
            form.save()

            next_img = get_random_image_without_tags()
            if next_img:
                return HttpResponseRedirect(reverse('images:add_tags', args=(next_img.id, )))
            return HttpResponseRedirect(reverse('images:congratulations'))

    else:
        form = ImageForm()

    return render(request, 'images/add-tags.html', {'form': form, 'image': image})
