from django.test import TestCase
from django.contrib.auth.models import User

from .models import Order
from .utility import (
    order_form_from_request,
    extract_payment_intent_id,
    update_user_profile_from_order,
)


class TestOrderFormFromRequest(TestCase):
    """ Testing class for Order utility functions """

    form_data = {
        'full_name' : 'full_name',
        'email': 'email@example.com',
        'phone_number': 'phone_number',
        'gift_message': 'gift_message',
        'payment_street_address1': 'payment_street_address1',
        'payment_street_address2': 'payment_street_address2',
        'payment_town_or_city': 'payment_town_or_city',
        'payment_county': 'payment_county',
        'payment_postcode': 'payment_postcode',
        'payment_country': 'SE',
        'shipping_full_name': 'shipping_full_name',
        'shipping_street_address1': 'shipping_street_address1',
        'shipping_street_address2': 'shipping_street_address2',
        'shipping_town_or_city': 'shipping_town_or_city',
        'shipping_county': 'shipping_county',
        'shipping_postcode': 'shipping_postcode',
        'shipping_country': 'SE',
    }


    def test_valid_request_returns_valid_form(self):
        order_form = order_form_from_request(self.form_data)
        self.assertTrue(order_form.is_valid())


    def test_missing_fields_returns_invalid_form(self):
        new_form_data = {
            key: value
            for key, value in self.form_data.items()
            if key != 'email'
        }
        order_form = order_form_from_request(new_form_data)
        self.assertFalse(order_form.is_valid())
        self.assertEqual(order_form.errors['email'][0], 'This field is required.')


    def test_card_address_as_shipping_address_populates_fields(self):
        new_form_data = {
            key: value
            for key, value in self.form_data.items()
            if not key.startswith('shipping_')
        }
        new_form_data['use-card-address-as-shipping-address'] = 'on'
        order_form = order_form_from_request(new_form_data)
        self.assertTrue(order_form.is_valid())
        self.assertEqual(order_form.cleaned_data['shipping_full_name'], new_form_data['full_name'])


class TestExtractPaymentIntentID(TestCase):
    """ Testing class for Order utility functions """

    def test_extracts_payment_id(self):
        client_secret = 'xxx_secret_yyy'
        payment_intent_id = extract_payment_intent_id(client_secret)
        self.assertEqual(payment_intent_id, 'xxx')


class TestUpdateUserProfileFromOrder(TestCase):
    """ Testing class for Order utility functions """

    order_data = {
        'stripe_payment_id': 'stripe_payment_id',
        'status': 'submitted',
        'full_name' : 'full_name',
        'email': 'email@example.com',
        'phone_number': 'phone_number',
        'gift_message': 'gift_message',
        'payment_street_address1': 'payment_street_address1',
        'payment_street_address2': 'payment_street_address2',
        'payment_town_or_city': 'payment_town_or_city',
        'payment_county': 'payment_county',
        'payment_postcode': 'payment_postcode',
        'payment_country': 'SE',
        'shipping_full_name': 'shipping_full_name',
        'shipping_street_address1': 'shipping_street_address1',
        'shipping_street_address2': 'shipping_street_address2',
        'shipping_town_or_city': 'shipping_town_or_city',
        'shipping_county': 'shipping_county',
        'shipping_postcode': 'shipping_postcode',
        'shipping_country': 'SE',
    }

    user_data = {
        'username': 'username',
        'password': 'password',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
    }

    def test_update_user_profile_from_order(self):
        user = User.objects.create_user(**self.user_data)
        order = Order.objects.create(user_profile=user.profile, **self.order_data)

        # Empty before we fun our function
        self.assertEqual(user.profile.default_street_address1, None)

        update_user_profile_from_order(order)

        # Now contains the matching data
        self.assertEqual(user.profile.default_street_address1, self.order_data['payment_street_address1'])


    def test_update_user_profile_from_order_where_no_user(self):
        order = Order.objects.create(user_profile=None, **self.order_data)

        # This function should not fail if there is no profile
        update_user_profile_from_order(order)


