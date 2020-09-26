from django.urls import path

from . import views

urlpatterns = [
    path('', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
]
