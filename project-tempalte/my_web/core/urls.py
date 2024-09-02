from django.urls import path
from .views import *
from .views import about_page_view, terms_and_conditions
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", home_page_view, name="home"),
    path("about", about_page_view, name="about"),
    path('terms-and-conditions', views.terms_and_conditions, name='terms_and_conditions'),
    path('download-image/', views.download_image, name='download_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
