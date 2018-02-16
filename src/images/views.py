from django.views import generic
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .models import Image, get_random_image_without_tags
from .forms import ImageForm


class DetailView(generic.DetailView):
    model = Image
    template_name = 'images/image.html'


def add_tags(request, pk):
    image = Image.objects.get(pk=pk)

    if request.method == 'POST':
        form = ImageForm(request.POST, instance=image)

        if form.is_valid():
            form.save()

            next_img = get_random_image_without_tags()
            if next_img:
                return HttpResponseRedirect(reverse('images:add_tags', args=(next_img.id, )))

    else:
        form = ImageForm()

    return render(request, 'images/add-tags.html', {'form': form, 'image': image})
