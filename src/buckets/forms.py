from django import forms
from django.forms import modelformset_factory
from django.forms.formsets import BaseFormSet
from django.contrib.auth.models import User

from django.db.models import Q

from .models import Bucket, Label
from images.models import Image, Vote


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['name', 'project']

    def __init__(self, user=None, *args, **kwargs):
        super(BucketForm, self).__init__(*args, **kwargs)


class BucketAddLabelsForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['labels']

    def __init__(self, *args, **kwargs):
        super(BucketAddLabelsForm, self).__init__(*args, **kwargs)
        self.fields['labels'].queryset = Label.objects.filter(project=self.instance.project)


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

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('shared_users').queryset = User.objects.filter(~Q(pk=user.pk))
