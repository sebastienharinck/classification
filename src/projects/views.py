from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import Project
from .forms import ProjectForm, ProjectAddLabelForm

from buckets.models import Label


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)


class ProjectAddLabelsView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = ProjectAddLabelForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.project = Project.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', args=(self.kwargs.get('pk'),))
