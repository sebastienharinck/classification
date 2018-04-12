from django import forms

from .models import Project

from buckets.models import Label


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


class ProjectAddLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
