from django.contrib import admin

from .models import Series


class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(Series, SeriesAdmin)
