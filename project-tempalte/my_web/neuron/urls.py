# neuron/urls.py

from django.urls import path
from .views import UploadModelView, UploadSuccessView, ImageUploadView, PredictionResultView

urlpatterns = [
    path('upload/', UploadModelView.as_view(), name='upload_model'),
    path('upload/success/', UploadSuccessView.as_view(), name='upload_success'),
    path('upload/image/', ImageUploadView.as_view(), name='upload_image'),
    path('upload/prediction/', PredictionResultView.as_view(), name='prediction_result'),
]
