from django.urls import path

from . import views

urlpatterns = [
    path('add/<product_id>', views.add_to_shopping_basket, name='add_to_shopping_basket'),
]
