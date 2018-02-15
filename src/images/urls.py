from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail')
]
