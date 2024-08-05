from django.shortcuts import render

# Create your views here.
# neuron/views.py
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.shortcuts import render
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from .forms import UploadModelForm, UploadImageForm
from django.views.generic.base import TemplateView


class UploadModelView(FormView):
    template_name = 'neuron/upload_model.html'
    form_class = UploadModelForm
    success_url = reverse_lazy('upload_success')

    def form_valid(self, form):
        # Uložení nahraného souboru
        model_file = form.cleaned_data['model_file']
        fs = FileSystemStorage()
        filename = fs.save(model_file.name, model_file)
        model_file_path = fs.path(filename)  # Získání cesty k souboru modelu

        # Uložení cesty k modelu do session
        self.request.session['model_file_path'] = model_file_path

        # Přidání URL nahraného souboru do kontextu
        self.extra_context = {'uploaded_file_url': fs.url(filename)}

        return super().form_valid(form)

class UploadSuccessView(TemplateView):
    template_name = 'neuron/upload_success.html'

# Třída pro nahrání obrázku a spuštění predikce
class ImageUploadView(FormView):
    template_name = 'neuron/upload_image.html'
    form_class = UploadImageForm
    success_url = reverse_lazy('prediction_result')

    def form_valid(self, form):
        # Uložení nahraného obrázku
        image_file = form.cleaned_data['image_file']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_file_path = fs.path(filename)

        # Načtení uloženého modelu
        model_file_path = self.request.session.get('model_file_path')
        if model_file_path is None:
            return self.form_invalid(form)  # Ošetření situace, kdy model_file_path je None

        model = load_model(model_file_path)

        # Předzpracování obrázku pro predikci
        img = image.load_img(image_file_path, target_size=(28, 28))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Spuštění predikce
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Uložení výsledku predikce do session
        self.request.session['prediction_result'] = predicted_class

        return super().form_valid(form)

# Třída pro zobrazení výsledku predikce
class PredictionResultView(TemplateView):
    template_name = 'neuron/prediction_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prediction_result = self.request.session.get('prediction_result', None)
        context['prediction_result'] = prediction_result
        return context