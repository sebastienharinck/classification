from django import forms

from .models import Tag


class ImageForm(forms.Form):
    tags = forms.MultipleChoiceField(
        choices=Tag.objects.all().values_list('id', 'name'),
        widget=forms.CheckboxSelectMultiple,
    )
