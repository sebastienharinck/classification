from django.urls import path
from . import views

app_name = 'buckets'

urlpatterns = [
    path('', views.BucketsListView.as_view(), name='list'),
    path('create/', views.BucketCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BucketDetailView.as_view(), name='detail'),
]
