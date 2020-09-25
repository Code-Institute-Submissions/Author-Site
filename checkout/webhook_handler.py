from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json
import stripe



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
        print('handle_payment_intent_succeeded', payment_intent)
        return HttpResponse(status=200)


    def handle_payment_intent_payment_failed(self, event):
        payment_intent = event.data.object
        print('handle_payment_intent_payment_failed', payment_intent)
        return HttpResponse(status=200)


    def unhandled_event(self, event):
        print(event.type, event)
        return HttpResponse(status=200)
