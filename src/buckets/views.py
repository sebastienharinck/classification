from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, TemplateView, ListView, CreateView, FormView
from django.shortcuts import reverse

from .models import Bucket, Label
from .forms import BucketForm, BucketAddLabelsForm


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

    def get_success_url(self):
        return reverse('buckets:list')


class BucketAddLabelsView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = BucketAddLabelsForm
    template_name = 'buckets/bucket_form.html'
    success_url = '/congratulations'

    def form_valid(self, form):
        obj = form.save(commit=False)
        bucket = Bucket.objects.filter(pk=self.kwargs.get('pk'), user=self.request.user)
        if not bucket.exists():
            return HttpResponseForbidden()
        obj.bucket = bucket.first()
        return super(BucketAddLabelsView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BucketAddLabelsView, self).get_form_kwargs()
        bucket = Bucket.objects.filter(pk=self.kwargs.get('pk'), user=self.request.user)
        kwargs['bucket'] = bucket.first()
        return kwargs
