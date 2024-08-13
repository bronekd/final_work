# neuron/forms.py

from django import forms

class UploadModelForm(forms.Form):
    model_file = forms.FileField(
        label='Vyberte model k nahrání',
        widget=forms.FileInput(attrs={'class': 'form-control', 'id':'inputGroupFile01', 'placeholder': 'Vlož model'}) # toto odkomentuj pro css boostrap
    )

class UploadImageForm(forms.Form):
    image_file = forms.ImageField(label='Vyberte obrázek k vyhodnocení')

class ModelUploadForm(forms.Form):
    model_file = forms.FileField()