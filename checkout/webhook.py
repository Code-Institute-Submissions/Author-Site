from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .webhook_handler import Stripe_WebHook_Handler

import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
@csrf_exempt
def stripe_webhook_handler(request):
    """
    Handle the incoming request and pass it to the Handler class
    """

    stripe_webhook_handler = Stripe_WebHook_Handler(request, settings.STRIPE_WEBHOOK_SECRET)
    return stripe_webhook_handler.process_request()
