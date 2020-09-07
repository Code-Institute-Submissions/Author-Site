from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_or_update_shopping_basket, name='view_or_update_shopping_basket'),
    path('add/<product_id>', views.add_to_shopping_basket, name='add_to_shopping_basket'),
]
