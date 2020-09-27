from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_fan_art, name='all_fan_art'),
    path('user_fan_art', views.user_fan_art, name='user_fan_art'),
    path('add_fan_art', views.add_fan_art, name='add_fan_art'),
    path('edit_fan_art/<art_id>', views.edit_fan_art, name='edit_fan_art'),
    path('delete_fan_art/<art_id>', views.delete_fan_art, name='delete_fan_art'),
]
