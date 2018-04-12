from django.views.generic import ListView
from .models import Project


class ProjectsListView(ListView):
    model = Project