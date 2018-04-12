from django.urls import path
from . import views

app_name = 'projects'


urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/add-labels/', views.ProjectAddLabelsView.as_view(), name='add-labels'),
]