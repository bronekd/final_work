from django.shortcuts import render


def home_page_view(request):
    return render(request, "pages/home.html")


def about_page_view(request):
    return render(request, "pages/about.html")


def terms_and_conditions(request):
    return render(request, 'pages/terms_and_conditions.html')