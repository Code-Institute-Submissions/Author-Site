from django.urls import path

from . import views
from .webhook import stripe_webhook_handler

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('stripe/', stripe_webhook_handler, name='stripe')
]
