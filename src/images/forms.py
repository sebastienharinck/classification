from django.forms import ModelForm

from .models import Vote, Bucket


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['tags']


class BucketForm(ModelForm):
    class Meta:
        model = Bucket
        fields = ['name']

    def __init__(self, user=None, *args, **kwargs):
        super(BucketForm, self).__init__(*args, **kwargs)
