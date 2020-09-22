from django.urls import path

from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('validate/', views.validate_form_and_update_payment_intent, name='validate'),
]
