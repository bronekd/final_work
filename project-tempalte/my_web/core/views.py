from django.shortcuts import render


def home_page_view(request):
    return render(request, "pages/home.html")


def about_page_view(request):
    return render(request, "pages/about.html")


def terms_and_conditions(request):
    return render(request, 'pages/terms_and_conditions.html')


from django.http import HttpResponse
from django.conf import settings
import os

def download_image(request):
    image_path = os.path.join(settings.MEDIA_ROOT, 'vzor/Kolecko_01.png')
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="Kolecko_01.png"'
        return response
    else:
        return HttpResponse('Soubor nenalezen.', status=404)
