from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'series',
        'product_type',
        'price',
        'in_stock',
        'isbn',
    )

    list_display_links = (
        'name',
        'series',
        'product_type',
        'price',
        'in_stock',
        'isbn',
    )

    search_fields = (
        'name',
        'series',
        'product_type',
        'price',
        'in_stock',
        'isbn',
    )

    list_per_page = 25

    fieldsets = (
        ('All Products', {
            'fields': ('name', 'series', 'product_type',
            'price', 'in_stock', 'image', 'description',
            'shipping', 'recommended_audience_age',)
        }),
        ('All Books', {
            'fields': ('author', 'publish_date', 'publisher',
            'isbn', 'synopsis')
        }),
        ('Physical Books & E-books', {
            'fields': ('page_count',)
        }),
        ('Audio Books', {
            'fields': ('run_time', 'narrator')
        }),
    )


admin.site.register(Product, ProductAdmin)
