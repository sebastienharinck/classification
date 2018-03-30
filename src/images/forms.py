from django.forms import ModelForm

from .models import *
from buckets.models import *


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['label']

    def __init__(self, user=None, bucket=None, *args, **kwargs):
        self.image = kwargs.pop('image')
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['label'].queryset = Label.objects.filter(bucket__image=self.image.id)


