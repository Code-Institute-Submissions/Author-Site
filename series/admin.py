from django.contrib import admin

from .models import Series


class SeriesAdmin(admin.ModelAdmin):
    """ Admin class for Series model """
    list_display = (
        'name',
    )

    def has_delete_permission(self, request, series=None):
        """ Prevents a series from being deleted """
        return False


admin.site.register(Series, SeriesAdmin)
