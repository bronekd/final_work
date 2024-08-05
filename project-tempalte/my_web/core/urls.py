from django.urls import path
from .views import *


urlpatterns = [
    path("", home_page_view, name="home"),
    path("about", about_page_view, name="about"),
]