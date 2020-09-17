from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from .forms import OrderForm
from shopping_basket.context_processors import shopping_basket

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """ Returns the page where users fill out the order form """

    # Get the current shopping basket
    current_basket = shopping_basket(request)['shopping_basket']

    # Check the users has items in their shopping basket
    if not current_basket['products']:
        messages.info(
            request,
            'Hey, looks like your bag is empty! Why not check out the shop?'
        )
        redirect_url = reverse('products')
        return redirect(redirect_url)

    # Calculate total for stripe (with no decimal places)
    stripe_total = round(current_basket['grand_total'] * 100)

    # Stripe payment intent
    payment_intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Create our order form
    order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': payment_intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)
