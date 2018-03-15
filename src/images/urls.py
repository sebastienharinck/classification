from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('<int:pk>/', views.ImageDetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.VoteCreateView.as_view(), name='vote'),
]
