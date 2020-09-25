from django.conf import settings
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST

from .forms import Order, OrderForm
from .models import OrderLineItem
from .utility import order_form_from_request, extract_payment_intent_id
from shopping_basket.context_processors import shopping_basket

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
def validate_form_and_update_payment_intent(request):
    """
    A view to validate the users payment form, then update
    the payment intent.
    """
    order_form = order_form_from_request(request)

    # Validate the form
    if order_form.is_valid():
        # Get the current shopping basket
        current_basket = shopping_basket(request)['shopping_basket']

        # Check the users has items in their shopping basket
        if not current_basket['products']:
            messages.info(
                request,
                'Hey, looks like your bag is empty! Why not check out the shop?'
            )
            # TODO: find alternative error handling for this
            # redirect_url = reverse('products')
            # return redirect(redirect_url)

        # Calculate total for stripe (with no decimal places)
        stripe_total = round(current_basket['grand_total'] * 100)

        # Create the payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            shipping={
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
            },
            metadata={}
        )

        context = {
            'client_secret': payment_intent.client_secret
        }

        return JsonResponse(context)

    else:
        print(order_form.errors)

    return HttpResponse(status=200)


    # TODO: Update payment intent with other info
    # TODO: Wrap in try-catch
    # TODO: Handle validation error



def checkout(request):
    """ Returns the page where users fill out the order form """

    if request.method == 'POST':
        order_form = order_form_from_request(request)
        payment_intent_id = extract_payment_intent_id(request.POST.get('client_secret'))

        # Get the shopping basket items
        try:
            current_basket = shopping_basket(request)['shopping_basket']
        except Http404:
            # Critical problem - customer has already paid
            messages.error(request,
                f"One of the products in your bag wasn't found in our database. \
                Please email us with this reference number {payment_intent_id}!"
            )
            print(payment_intent_id)
            # TODO: Empty the shopping basket
            redirect_url = reverse('view_or_update_shopping_basket')
            return redirect(redirect_url)

        # Critical problem - form already validated
        if not order_form.is_valid():
            messages.error(request, f'Hey, something went really wrong, \
                please email us with this reference number {payment_intent_id}')
            print(payment_intent_id, order_form.errors)
            # TODO: Empty the shopping basket

            redirect_url = reverse('view_or_update_shopping_basket')
            return redirect(redirect_url)

        # Creating the order from the order form and the shopping basket
        order = order_form.save(commit=False)
        order.stripe_payment_id = payment_intent_id
        if request.user.is_authenticated:
            order.user_profile = request.user.profile
        order.status = 'submitted'
        order.save()

        # Creating our line items
        for entry in current_basket['products']:
            order_line_item = OrderLineItem(
                order=order,
                product=entry['product'],
                quantity=entry['amount'],
                price=entry['product'].price,
                shipping=entry['product'].shipping,
            )
            order_line_item.save()

        # Emptying the shopping basket
        request.session['shopping_basket'] = {}

        messages.success(request, f'Order successfully processed! \
            Your order number is {order.order_number}. A confirmation \
            email will be sent to {order.email}'
        )

        # TODO: handle if order already exists (race condition)
        # TODO: handle 'save info'
        # TODO: redirect to the order page for the order (if user is logged in)
        # TODO: Send a confirmation email to the user that the porder went through

        return redirect(reverse('checkout_success', args=[order.order_number]))

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

    # Create our order form
    order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Redirect users to a success landing page, displaying their order.
    """

    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)