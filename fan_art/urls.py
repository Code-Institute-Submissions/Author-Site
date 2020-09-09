from django.urls import path

from . import views

urlpatterns = [
    path('', views.fan_art_gallery, name='fan_art_gallery'),
]
