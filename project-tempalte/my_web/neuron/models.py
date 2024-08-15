from django.db import models

# Create your models here.
# neuron/models.py
from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    model_file = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name

class ImagePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    model_name = models.CharField(max_length=255)
    predicted_class = models.IntegerField()
    prediction_timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)  # Přidané pole pro popis

    def __str__(self):
        return f"Prediction by {self.model_name} on {self.image_file.name}"