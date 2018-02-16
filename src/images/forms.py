from django.forms import ModelForm

from .models import Image, Vote


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['tags']


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['tags']
