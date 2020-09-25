from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Order

import json
import stripe
import time



class Stripe_WebHook_Handler:
    """
    Handles and processes the stripe webhook request.
    """

    def __init__(self, request, endpoint_secret):
        self.request = request
        self.endpoint_secret = endpoint_secret
        # Dictionary of the events we handle
        self.event_handlers = {
            'payment_intent.succeeded': self.handle_payment_intent_succeeded,
            'payment_intent.payment_failed': self.handle_payment_intent_payment_failed,
        }


    def  process_request(self):
        event = None

        try:
            event = stripe.Webhook.construct_event(
                self.request.body,
                self.request.META['HTTP_STRIPE_SIGNATURE'],
                self.endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        event_handler = self.event_handlers.get(event.type, self.unhandled_event)

        return event_handler(event)


    def handle_payment_intent_succeeded(self, event):
        payment_intent = event.data.object

        for attempt in range(5):
            try:
                order = Order.objects.get(stripe_payment_id=payment_intent.id)
            except Order.DoesNotExist:
                # We did not find the order in this attempt
                time.sleep(1)
                continue

            # We found the order
            order.status = 'paid'
            order.save()
            return HttpResponse(status=200)

        # We did not find the order at all
        # TODO: create the order

        return HttpResponse(status=200)


    def handle_payment_intent_payment_failed(self, event):
        payment_intent = event.data.object

        for attempt in range(5):
            try:
                order = Order.objects.get(stripe_payment_id=payment_intent.id)
            except Order.DoesNotExist:
                # We did not find the order in this attempt
                time.sleep(1)
                continue

            # We found the order
            order.status = 'payment_failed'
            order.save()
            # TODO: send the user an email
            return HttpResponse(status=200)

        # We did not find the order at all

        return HttpResponse(status=500)


    def unhandled_event(self, event):
        print(event.type, event)
        return HttpResponse(status=200)
