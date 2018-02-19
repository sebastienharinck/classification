from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .forms import VoteForm
from .models import Image, get_random_image_with_no_vote


class HomeView(TemplateView):
    template_name = 'images/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_img = get_random_image_with_no_vote()
        if next_img:
            context['next_img'] = next_img.id
        return context


class DetailView(DetailView):
    model = Image
    template_name = 'images/image.html'


class CongratulationsView(TemplateView):
    template_name = 'images/congratulations.html'


@login_required
def vote(request, pk):
    image = Image.objects.get(pk=pk)

    if request.method == 'POST':
        form = VoteForm(request.POST)

        if form.is_valid():
            vote = form.save(commit=False)
            vote.image = image
            vote.user = request.user
            vote.save()
            form.save_m2m()

            next_img = get_random_image_with_no_vote()
            if next_img:
                return HttpResponseRedirect(reverse('images:vote', args=(next_img.id,)))
            return HttpResponseRedirect(reverse('images:congratulations'))

    else:
        form = VoteForm()

    return render(request, 'images/vote.html', {'form': form, 'image': image})
