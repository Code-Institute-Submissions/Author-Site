from django.contrib import admin

from .models import Series


class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

    def has_delete_permission(self, request, series=None):
        return False


admin.site.register(Series, SeriesAdmin)
