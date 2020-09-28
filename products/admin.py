from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'series',
        'product_type',
        'price',
        'in_stock',
        'list_in_shop',
    )

    list_display_links = (
        'name',
        'series',
        'product_type',
        'price',
        'in_stock',
        'list_in_shop',
    )

    search_fields = (
        'name',
        'series',
        'product_type',
        'price',
        'in_stock',
        'list_in_shop',
        'isbn',
    )

    list_per_page = 25

    list_filter = (
        'list_in_shop',
        'in_stock'
    )


    fieldsets = (
        ('All Products', {
            'fields': ('name', 'series', 'product_type',
            'price', 'in_stock', 'list_in_shop', 'image', 'description',
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

    def has_delete_permission(self, request, product=None):
        return False


admin.site.register(Product, ProductAdmin)
