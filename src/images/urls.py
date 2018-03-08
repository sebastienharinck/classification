from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('buckets/', views.BucketsListView.as_view(), name='buckets'),
    path('buckets/create/', views.BucketCreateView.as_view(), name='bucket_create'),
    path('buckets/<int:pk>/', views.BucketDetailView.as_view(), name='bucket_detail'),
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.ImageDetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('congratulations/', views.CongratulationsView.as_view(), name='congratulations'),
]
