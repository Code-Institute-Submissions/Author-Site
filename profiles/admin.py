from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'default_street_address1',
        'default_postcode',
        'default_country',
    )

    list_display_links = (
        'user',
        'default_street_address1',
        'default_postcode',
        'default_country',
    )

    search_fields = (
        'user',
        'default_street_address1',
        'default_postcode',
        'default_country',
    )

    list_per_page = 25

admin.site.register(UserProfile, UserProfileAdmin)