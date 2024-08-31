from django import forms
import django_filters
from .models import ImagePrediction

class ImagePredictionFilter(django_filters.FilterSet):
    model_name = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ImagePrediction
        fields = ['model_name']


"""'predicted_class': ['exact'],
            'prediction_timestamp': ['year__gt'],
            'description': ['icontains'],"""