from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('congratulations/', views.CongratulationsView.as_view(), name='congratulations'),
]
