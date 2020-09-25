from django.urls import path

from . import views
from .webhook import stripe_webhook_handler

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('validate/', views.validate_form_and_update_payment_intent, name='validate'),
    path('stripe/', stripe_webhook_handler, name='stripe')
]
