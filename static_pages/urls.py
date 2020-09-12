from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('magic_door', views.magic_door, name='magic_door'),
    path('parma_ham', views.parma_ham, name='parma_ham'),
]
