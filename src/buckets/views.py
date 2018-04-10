from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.shortcuts import reverse
from django.db.models import Q

from .forms import *

from images.models import *


class BucketsListView(LoginRequiredMixin, ListView):
    model = Bucket

    def get_queryset(self):
        return Bucket.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['shared_buckets'] = Bucket.objects.filter(shared_users=self.request.user)
        print(context['shared_buckets'])
        return context


class BucketDetailView(LoginRequiredMixin, DetailView):
    model = Bucket

    def get_context_data(self, *args, **kwargs):
        context = super(BucketDetailView, self).get_context_data(*args, **kwargs)
        bucket = Bucket.objects.get(pk=self.kwargs.get('pk'))
        context['images'] = Image.objects.filter(bucket=bucket.id)[0:20]
        # context['next_img'] = get_random_image_with_no_vote(bucket)
        return context


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

    def get_success_url(self):
        return reverse('buckets:detail', args=(self.kwargs.get('pk'),))


class VoteByLabelsView(LoginRequiredMixin, FormView):
    template_name = 'buckets/bucket_form_vote_by_labels.html'
    form_class = VoteFormSet
    images = None

    def get_form_kwargs(self):
        kwargs = super(VoteByLabelsView, self).get_form_kwargs()
        random_img = get_random_sample_image_with_no_vote(self.kwargs.get('label'), 8, self.request.user)
        if random_img:
            self.form_class.extra = len(random_img)
            self.images = Image.objects.filter(pk__in=random_img)
            kwargs['images'] = self.images
        else:
            self.form_class.extra = 0

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.images
        context['label'] = Label.objects.get(pk=self.kwargs.get('label'))
        return context

    def form_valid(self, form):
        form.is_valid()
        for f in form:
            obj = f.save(commit=False)
            obj.user = self.request.user
            obj.label = Label.objects.get(pk=self.kwargs.get('label'))
            print(obj)
            obj.save()

        return super(VoteByLabelsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('buckets:vote_by_labels', kwargs={'bucket': self.kwargs.get('bucket'), 'label': self.kwargs.get('label')})


"""
todo : https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html
"""
class UploadView(LoginRequiredMixin, FormView):
    template_name = 'buckets/bucket_form.html'
    form_class = UploadForm

    def form_valid(self, form):
        bucket = Bucket.objects.get(pk=self.kwargs.get('pk'), user=self.request.user)
        files = self.request.FILES.getlist('files')

        for file in files:
            Image.objects.create(file=file, bucket=bucket)
        return super(UploadView, self).form_valid(form)

    def get_success_url(self):
        return reverse('buckets:detail', args=(self.kwargs.get('pk'),))


# todo : securize
class ImagesListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'buckets/bucket_images.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'images'
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.filter(bucket=self.kwargs.get('pk'))


class BucketInviteUser(LoginRequiredMixin, FormView):
    template_name = 'buckets/bucket_form.html'
    form_class = BucketInviteUserForm

    def form_valid(self, form):
        bucket = Bucket.objects.get(pk=self.kwargs.get('pk'), user=self.request.user)
        form = BucketInviteUserForm(self.request.POST or None, instance=bucket)
        if form.is_valid():
            form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('buckets:list')
