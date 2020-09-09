from django.contrib import admin
from .models import FanArt


class FanArtAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name_plural = 'Fan Art'

    list_display = (
        'user_profile',
        'title',
        'series',
        'publish_date',
        'is_approved',
    )

    list_display_links = (
        'user_profile',
        'title',
        'series',
        'publish_date',
    )

    search_fields = (
        'is_approved',
        'user_profile',
        'series',
    )

    list_per_page = 25


admin.site.register(FanArt, FanArtAdmin)
