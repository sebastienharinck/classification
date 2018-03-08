from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('buckets/', views.BucketsListView.as_view(), name='buckets'),
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.ImageDetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('congratulations/', views.CongratulationsView.as_view(), name='congratulations'),
]
