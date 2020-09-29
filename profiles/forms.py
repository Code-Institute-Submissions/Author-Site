from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """ Form to update UserProfile instance """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove auto-generated
        labels and set autofocus
        """
        super().__init__(*args, **kwargs)

        # AUTOFOCUS
        self.fields['default_street_address1'].widget.attrs['autofocus'] = True

        # CUSTOMIZING THE FORM FIELDS
        for fieldname, field in self.fields.items():
            if fieldname != 'default_country':
                if field.required:
                    placeholder = f'{field.label} *'
                else:
                    placeholder = field.label

                field.widget.attrs['placeholder'] = placeholder

            field.label = False


class UserForm(forms.ModelForm):
    """ Form to update UserProfile instance """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels
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
            field.help_text = False
