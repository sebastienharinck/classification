from django import forms

from .models import Bucket, Label


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
