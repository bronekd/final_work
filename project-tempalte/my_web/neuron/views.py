
# neuron/views.py

from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from tensorflow.keras.models import load_model
from .forms import UploadModelForm, UploadImageForm
from .models import UserModel
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import UserModel, ImagePrediction
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from .models import UserModel, ImagePrediction
from .forms import UploadImageForm
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from .models import ImagePrediction
from django.shortcuts import render
from .models import ImagePrediction
from .filters import ImagePredictionFilter
from .models import ImagePrediction


class UploadModelView(LoginRequiredMixin, FormView):
    template_name = 'neuron/upload_model.html'
    form_class = UploadModelForm
    success_url = reverse_lazy('upload_success')

    def form_valid(self, form):
        # Uložení modelu do databáze
        model_instance = form.save(commit=False)
        model_instance.user = self.request.user
        model_instance.model_name = form.cleaned_data['model_file'].name
        model_instance.save()

        # Uložení cesty k modelu do session
        self.request.session['model_file_path'] = model_instance.model_file.path

        return super().form_valid(form)

class UserModelListView(LoginRequiredMixin, ListView):
    model = UserModel
    template_name = 'neuron/user_models.html'
    context_object_name = 'user_models'

    def get_queryset(self):
        return UserModel.objects.filter(user=self.request.user)




""" Stará funkční class
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

"""

class UploadSuccessView(TemplateView):
    template_name = 'neuron/upload_success.html'



"""
# Třída pro nahrání obrázku a spuštění predikce stará a funkční
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
        #self.request.session['prediction_result'] = predicted_class
        self.request.session['prediction_result'] = int(predicted_class)

        return super().form_valid(form)
"""
# neuron/views.py

""" # funkční kod ale bude vylepšen níze 
class ImageUploadView(LoginRequiredMixin, FormView):
    template_name = 'neuron/upload_image.html'
    form_class = UploadImageForm
    success_url = reverse_lazy('prediction_result')

    def form_valid(self, form):
        # Uložení nahraného obrázku
        image_file = form.cleaned_data['image_file']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_file_path = fs.path(filename)

        # Načtení modelu podle ID z GET parametrů nebo session
        model_id = self.request.GET.get('model_id')
        if model_id:
            model_instance = get_object_or_404(UserModel, id=model_id, user=self.request.user)
            model_file_path = model_instance.model_file.path
            model_name = model_instance.model_name
        else:
            model_file_path = self.request.session.get('model_file_path')
            model_name = "Unknown"

        if model_file_path is None:
            return self.form_invalid(form)

        model = load_model(model_file_path)

        # Předzpracování obrázku pro predikci
        img = image.load_img(image_file_path, target_size=(28, 28))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Spuštění predikce
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Uložení výsledku predikce do databáze
        ImagePrediction.objects.create(
            user=self.request.user,
            image_file=image_file,
            model_name=model_name,
            predicted_class=int(predicted_class)
        )

        # Uložení výsledku predikce do session
        self.request.session['prediction_result'] = int(predicted_class)

        return super().form_valid(form)

"""

class ImageUploadView(LoginRequiredMixin, FormView):
    template_name = 'neuron/upload_image.html'
    form_class = UploadImageForm
    success_url = reverse_lazy('prediction_result')

    def form_valid(self, form):
        # Uložení nahraného obrázku a popisu
        image_file = form.cleaned_data['image_file']
        description = form.cleaned_data['description']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_file_path = fs.path(filename)

        # Načtení modelu podle ID z GET parametrů
        model_id = self.request.GET.get('model_id')
        if model_id:
            model_instance = get_object_or_404(UserModel, id=model_id, user=self.request.user)
            model_file_path = model_instance.model_file.path
            model_name = model_instance.model_name
        else:
            model_file_path = self.request.session.get('model_file_path')
            if model_file_path:
                model_instance = UserModel.objects.filter(model_file=model_file_path).first()
                model_name = model_instance.model_name if model_instance else "Unknown"
            else:
                model_name = "Unknown"
                model_file_path = None

        if model_file_path is None:
            return self.form_invalid(form)

        model = load_model(model_file_path)

        # Předzpracování obrázku pro predikci
        img = image.load_img(image_file_path, target_size=(28, 28))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Spuštění predikce
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Uložení výsledku predikce do databáze
        ImagePrediction.objects.create(
            user=self.request.user,
            image_file=image_file,
            model_name=model_name,
            predicted_class=int(predicted_class),
            description=description
        )

        # Uložení výsledku predikce do session
        self.request.session['prediction_result'] = int(predicted_class)

        return super().form_valid(form)


# Třída pro zobrazení výsledku predikce
class PredictionResultView(TemplateView):
    template_name = 'neuron/prediction_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prediction_result = self.request.session.get('prediction_result', None)
        context['prediction_result'] = prediction_result
        return context


# neuron/views.py


class ImagePredictionListView(LoginRequiredMixin, ListView):
    model = ImagePrediction
    template_name = 'neuron/image_predictions.html'
    context_object_name = 'predictions'
    paginate_by = 10  # Počet položek na stránku

    def get_queryset(self):
        return ImagePrediction.objects.filter(user=self.request.user).order_by('-prediction_timestamp')

"""#filtr pro predikci
def prediction_list(request):
    filter = ImagePredictionFilter(request.GET, queryset=ImagePrediction.objects.all())
    return render(request, 'image_predictions.html', {'filter': filter})
"""
# neuron/views.py
# views.py

from django.views.generic import ListView
from django.shortcuts import render
from .models import ImagePrediction
from .forms import ImagePredictionFilterForm

class ImagePredictionFilterView(ListView):
    model = ImagePrediction
    template_name = 'neuron/image_predictions_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ImagePredictionFilterForm(self.request.GET)
        if form.is_valid():
            model_name = form.cleaned_data.get('model_name')
            predicted_class = form.cleaned_data.get('predicted_class')
            description = form.cleaned_data.get('description')

            if model_name:
                queryset = queryset.filter(model_name__icontains=model_name)
            if predicted_class:
                queryset = queryset.filter(predicted_class=predicted_class)
            if description:
                queryset = queryset.filter(description__icontains=description)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ImagePredictionFilterForm(self.request.GET)
        return context


# řešení javascript
from django.http import JsonResponse
from .models import ImagePrediction

def model_name_autocomplete(request):
    if 'term' in request.GET:
        qs = ImagePrediction.objects.filter(model_name__icontains=request.GET.get('term'))
        names = list(qs.values_list('model_name', flat=True).distinct())
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


