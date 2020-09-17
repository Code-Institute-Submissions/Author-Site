from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'gift_message',
            'payment_street_address1', 'payment_street_address2',
            'payment_town_or_city', 'payment_county',
            'payment_postcode', 'payment_country',
            'shipping_full_name', 'shipping_street_address1',
            'shipping_street_address2', 'shipping_town_or_city',
            'shipping_county', 'shipping_postcode', 'shipping_country',
        )

    def __init__(self, *args, **kwargs):
        """
        Adding placeholder values and removing labels
        """
        super().__init__(*args, **kwargs)

        # AUTOFOCUS
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # CUSTOMIZING THE FORM FIELDS
        for fieldname, field in self.fields.items():
            if fieldname not in ['payment_country', 'shipping_country']:
                if field.required:
                    placeholder = f'{field.label} *'
                else:
                    placeholder = field.label

                field.widget.attrs['placeholder'] = placeholder

            field.label = False
