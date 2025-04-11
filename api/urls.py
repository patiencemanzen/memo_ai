from django.urls import path
from .views import UploadMultipleImagesView

urlpatterns = [
    path('upload/', UploadMultipleImagesView.as_view(), name='upload-images'),
]
