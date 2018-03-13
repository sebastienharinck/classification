from django.forms import ModelForm

from .models import *
from buckets.models import *


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['labels']

    def __init__(self, image=None, user=None, bucket=None, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['labels'].queryset = Label.objects.filter(bucket__image=image.id)


