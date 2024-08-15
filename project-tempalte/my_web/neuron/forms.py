# neuron/forms.py

from django import forms

from django import forms
from .models import UserModel, ImagePrediction
from tensorflow.keras.models import load_model
import os

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['model_file']

    def clean_model_file(self):
        model_file = self.cleaned_data['model_file']

        # Validace souboru
        if not model_file.name.endswith('.h5'):
            raise forms.ValidationError("Nahraný soubor musí být Keras/TensorFlow model s příponou .h5")

        # Pokus o načtení modelu pro ověření jeho platnosti
        try:
            temp_path = '/tmp/' + model_file.name
            with open(temp_path, 'wb+') as temp_file:
                for chunk in model_file.chunks():
                    temp_file.write(chunk)
            load_model(temp_path)
            os.remove(temp_path)
        except Exception as e:
            raise forms.ValidationError(f"Nahraný soubor není platný Keras/TensorFlow model: {str(e)}")

        return model_file

""" stará funkční class 
class UploadModelForm(forms.Form):
    model_file = forms.FileField(
        label='Vyberte model k nahrání',
        widget=forms.FileInput(attrs={'class': 'form-control', 'id':'inputGroupFile01', 'placeholder': 'Vlož model'}) # toto odkomentuj pro css boostrap
    )
"""
""" # funkční kod ale rozšíříme jej.
class UploadImageForm(forms.Form):
    image_file = forms.ImageField(label='Vyberte obrázek k vyhodnocení')
"""
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = ImagePrediction
        fields = ['image_file', 'description']  # Přidáno pole pro popis

    def clean_description(self):
        description = self.cleaned_data.get('description')
        # Můžeš přidat další validace pro popis zde, pokud je to potřeba
        return description



class ModelUploadForm(forms.Form):
    model_file = forms.FileField()