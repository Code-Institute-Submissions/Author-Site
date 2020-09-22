from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.decorators.http import require_POST

from .forms import OrderForm
from shopping_basket.context_processors import shopping_basket

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
def validate_form_and_update_payment_intent(request):
    """
    A view to validate the users payment form, then update
    the payment intent.
    """

    # Convert QueryDict to Dict
    post_data = request.POST.dict()

    # Check use card address as shipping address
    if post_data['use-card-address-as-shipping-address'] == 'true':

        # Populate shipping address fields with payment address details
        shipping_mapping = {
            'shipping_full_name': 'full_name',
            'shipping_street_address1': 'payment_street_address1',
            'shipping_street_address2': 'payment_street_address2',
            'shipping_town_or_city': 'payment_town_or_city',
            'shipping_country': 'payment_country',
            'shipping_postcode': 'payment_postcode',
            'shipping_county': 'payment_county',
        }

        for shipping_field, payment_field in shipping_mapping.items():
            post_data[shipping_field] = post_data[payment_field]

    # Creating the order form for validation
    order_form = OrderForm(post_data)

    # Validate the form
    if order_form.is_valid():
        payment_intent_id = request.POST.get('client_secret').split('_secret')[0]

        # Update the payment intent
        stripe.PaymentIntent.modify(payment_intent_id, shipping={
            "name": order_form.cleaned_data['shipping_full_name'],
            "phone": order_form.cleaned_data['phone_number'],
            "address": {
                "line1": order_form.cleaned_data['shipping_street_address1'],
                "line2": order_form.cleaned_data['shipping_street_address2'],
                "city": order_form.cleaned_data['shipping_town_or_city'],
                "country": order_form.cleaned_data['shipping_country'],
                "postal_code": order_form.cleaned_data['shipping_postcode'],
                "state": order_form.cleaned_data['shipping_county'],
            }
        }, metadata={})

        print('sucess')
    else:
        print(order_form.errors)

    return HttpResponse(status=200)


    # TODO: Update payment intent with other info
    # TODO: Wrap in try-catch
    # TODO: Handle validation error



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
