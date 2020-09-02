from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)

        # AUTOFOCUS
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        # CUSTOMIZING THE FORM FIELDS
        for fieldname, field in self.fields.items():
            if fieldname != 'default_country':
                if field.required:
                    placeholder = f'{field.label} *'
                else:
                    placeholder = field.label

                field.widget.attrs['placeholder'] = placeholder

            field.label = False
