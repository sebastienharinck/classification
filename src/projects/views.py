from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Project


class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)