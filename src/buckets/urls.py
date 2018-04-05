from django.urls import path
from . import views

app_name = 'buckets'

urlpatterns = [
    path('', views.BucketsListView.as_view(), name='list'),
    path('create/', views.BucketCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BucketDetailView.as_view(), name='detail'),
    path('<int:pk>/images/', views.ImagesListView.as_view(), name='images'),
    path('<int:pk>/add-labels/', views.BucketAddLabelsView.as_view(), name='add_labels'),
    path('<int:bucket>/vote-by-labels/<int:label>/', views.VoteByLabelsView.as_view(), name='vote_by_labels'),
    path('<int:pk>/add-images/', views.UploadView.as_view(), name='add_images'),
    path('<int:pk>/invite-user/', views.BucketInviteUser.as_view(), name='invite_user'),
]
