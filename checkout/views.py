from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, reverse

from .forms import OrderForm

import os
import stripe


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


def checkout(request):
    """ Returns the page where users fill out the order form """

    # Check the users has items in their shopping basket
    shopping_basket = request.session.get('shopping_basket', {})
    if not shopping_basket:
        messages.info(
            request,
            'Hey, looks like your bag is empty! Why not check out the shop?'
        )
        redirect_url = reverse('products')
        return redirect(redirect_url)

    order_form = OrderForm()

    context = {
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)
