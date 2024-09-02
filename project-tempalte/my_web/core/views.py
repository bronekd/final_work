from django.shortcuts import render
from django.http import FileResponse

def home_page_view(request):
    return render(request, "pages/home.html")


def about_page_view(request):
    return render(request, "pages/about.html")


def terms_and_conditions(request):
    return render(request, 'pages/terms_and_conditions.html')



def download_model(request):
    file_path = 'path/to/your/model.h5'
    response = FileResponse(open(file_path, 'rb'))
    return response

def download_image(request):
    image_path = 'path/to/your/image.png'
    response = FileResponse(open(image_path, 'rb'))
    return response
