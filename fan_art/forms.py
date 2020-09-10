from django import forms
from django.contrib.auth.models import User
from .models import FanArt


class CreateFanArtForm(forms.ModelForm):

    class Meta:
        model = FanArt
        exclude = ('user_profile', 'is_approved', 'publish_date')

    def __init__(self, *args, **kwargs):
        """

        """
        super().__init__(*args, **kwargs)

        # CUSTOMIZING THE FORM FIELDS
        for fieldname, field in self.fields.items():
            if field.required:
                placeholder = f'{field.label} *'
            else:
                placeholder = field.label

            field.widget.attrs['placeholder'] = placeholder

            field.label = False


class UpdateFanArtForm(forms.ModelForm):

    class Meta:
        model = FanArt
        exclude = (
            'user_profile',
            'is_approved',
            'publish_date',
            'image',
        )

    def __init__(self, *args, **kwargs):
        """

        """
        super().__init__(*args, **kwargs)

        # CUSTOMIZING THE FORM FIELDS
        for fieldname, field in self.fields.items():
            if field.required:
                placeholder = f'{field.label} *'
            else:
                placeholder = field.label

            field.widget.attrs['placeholder'] = placeholder

            field.label = False
