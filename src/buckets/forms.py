import random

from django import forms
from django.forms import modelformset_factory
from django.db.models import Q
from django.forms.formsets import BaseFormSet

from .models import Bucket, Label
from images.models import Image, Vote


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['name']

    def __init__(self, user=None, *args, **kwargs):
        super(BucketForm, self).__init__(*args, **kwargs)


class BucketAddLabelsForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

    def __init__(self, bucket=None, *args, **kwargs):
        super(BucketAddLabelsForm, self).__init__(*args, **kwargs)


class UploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['image', 'choice']
        widgets = {'image': forms.HiddenInput()}

    def __init__(self, image=None, label=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields.get('image').initial = image


class BaseSelectDatesFormSet(BaseFormSet):
    def __init__(self, images=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = images
        for form in self.forms:
            form.empty_permitted = False

    def get_form_kwargs(self, index):
        kwargs = super(BaseSelectDatesFormSet, self).get_form_kwargs(index)
        kwargs['image'] = self.images[index]

        return kwargs

    def save(self, commit=False):
        pass


VoteFormSet = modelformset_factory(model=Vote, form=VoteForm, extra=8, formset=BaseSelectDatesFormSet)


class BucketInviteUserForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['shared_users']


def get_all_images_ids_with_no_vote(label, user=None):
    label = Label.objects.get(pk=label)

    q = Image.objects.filter(~Q(vote__in=Vote.objects.filter(label=label, user=user)), bucket=label.bucket)
    q = q.values_list('id', flat=True)

    return q


def get_random_image_with_no_vote(bucket):
    ids = get_all_images_ids_with_no_vote(bucket)
    if not ids:
        return False
    rand = random.choice(ids)
    return Image.objects.filter(pk=rand)


def get_random_sample_image_with_no_vote(label, number, user=None):
    ids = get_all_images_ids_with_no_vote(label, user)
    if not ids:
        return False
    ids_size = len(ids)
    if ids_size > number:
        rand = random.sample(list(ids), number)
    else:
        rand = random.sample(list(ids), ids_size)
    return Image.objects.filter(id__in=rand)
