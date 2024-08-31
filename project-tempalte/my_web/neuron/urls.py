# neuron/urls.py

from django.urls import path
from .views import (UploadModelView, UploadSuccessView, ImageUploadView, PredictionResultView,
                    UserModelListView, ImagePredictionListView)
from .views import ImagePredictionFilterView, model_name_autocomplete

urlpatterns = [
    path('upload/', UploadModelView.as_view(), name='upload_model'),
    path('upload/success/', UploadSuccessView.as_view(), name='upload_success'),
    path('upload/image/', ImageUploadView.as_view(), name='upload_image'),
    path('upload/prediction/', PredictionResultView.as_view(), name='prediction_result'),
    path('models/', UserModelListView.as_view(), name='user_models'),
    path('predictions/', ImagePredictionListView.as_view(), name='image_predictions'),
    path('predictions/filtr/', ImagePredictionFilterView.as_view(), name='search_image_prediction'),
    path('model-name-autocomplete/', model_name_autocomplete, name='model_name_autocomplete'),
]
