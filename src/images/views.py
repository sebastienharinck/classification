from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, CreateView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

from .forms import VoteForm
from .models import *

from buckets.models import *


class HomeView(TemplateView):
    template_name = 'images/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_img = get_random_image_with_no_vote()
        if next_img:
            context['next_img'] = next_img.id
        return context


class ImageDetailView(DetailView):
    model = Image
    template_name = 'images/image.html'


class VoteCreateView(LoginRequiredMixin, CreateView):
    model = Vote
    form_class = VoteForm
    template_name = 'images/vote_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        image = Image.objects.filter(pk=self.kwargs.get('pk'))
        bucket = Bucket.objects.filter(image=self.kwargs.get('pk')).first()
        if not image.exists():
            return HttpResponseForbidden()
        obj.image = image.first()
        obj.user = self.request.user
        obj.bucket = bucket
        return super(VoteCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(VoteCreateView, self).get_form_kwargs()
        image = Image.objects.get(pk=self.kwargs.get('pk'))
        bucket = Bucket.objects.filter(image=self.kwargs.get('pk')).first()
        kwargs['image'] = image
        kwargs['user'] = self.request.user
        kwargs['bucket'] = bucket
        return kwargs

    def get_success_url(self):
        image = Image.objects.get(pk=self.kwargs.get('pk'))
        next_image = get_random_image_with_no_vote(image.bucket)
        if next_image:
            return reverse('images:vote', args=(next_image.id,))
        return reverse('buckets:detail', args=(image.bucket.id,))

    def get_context_data(self, *args, **kwargs):
        context = super(VoteCreateView, self).get_context_data(*args, **kwargs)
        context['image'] = Image.objects.get(pk=self.kwargs.get('pk'))
        context['bucket'] = Bucket.objects.filter(image=self.kwargs.get('pk')).first()
        return context
