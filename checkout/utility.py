from .forms import OrderForm


def order_form_from_request(request):
    """
    A function to create an order form instance from request data
    """
    # Convert QueryDict to Dict
    post_data = request.POST.dict()

    # Check use card address as shipping address
    if post_data.get('use-card-address-as-shipping-address') == 'on':

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

    return order_form


def extract_payment_intent_id(client_secret):
    return client_secret.split('_secret')[0]
