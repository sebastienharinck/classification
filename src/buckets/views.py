from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, ListView, CreateView

from .models import Bucket
from .forms import BucketForm


class BucketsListView(LoginRequiredMixin, ListView):
    model = Bucket

    def get_queryset(self):
        return Bucket.objects.filter(user=self.request.user)


class BucketDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Bucket.objects.all()


class BucketCreateView(LoginRequiredMixin, CreateView):
    model = Bucket
    form_class = BucketForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(BucketCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BucketCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
