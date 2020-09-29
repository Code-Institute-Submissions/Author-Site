from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInLine(admin.TabularInline):
    """
    Admin class for order line items. Set as inline only,
    has no add or delete permission to prevent order modification post payment.
    """
    model = OrderLineItem
    extra = 0

    readonly_fields = (
        'product_name',
        'product_type',
        'quantity',
        'price',
        'shipping',
        'grand_total',
    )

    exclude = [
        'product',
    ]

    def has_delete_permission(self, request, order):
        """ Prevents order line items from being deleted """
        return False

    def has_add_permission(self, request, order):
        """ Prevents order line items from being added """
        return False

    def product_type(self, order_line):
        """ Returns the product type to display in the order line item """
        return order_line.product.get_product_type_display()

    def product_name(self, order_line):
        """ Returns the product name to display in the order line item """
        return order_line.product.name



class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for order. Line items set as inline only,
    """
    inlines = (OrderLineItemAdminInLine,)

    list_display = (
        'order_number',
        'status',
        'user_profile',
        'full_name',
        'email',
        'date',
    )

    list_display_links = (
        'order_number',
        'date',
        'user_profile',
        'status',
        'full_name',
        'email',
    )

    search_fields = (
        'order_number',
        'date',
        'stripe_payment_id',
        'user_profile',
        'status',
        'full_name',
        'email',
    )

    list_filter = (
        'status',
    )

    readonly_fields = ('order_number', 'date', 'stripe_payment_id',
                       'user_profile', 'price_total', 'shipping_total',
                       'grand_total', 'payment_street_address1',
                       'payment_street_address2', 'payment_town_or_city',
                       'payment_county', 'payment_postcode', 'payment_country')

    ordering = ('-date',)
    list_per_page = 25

    fieldsets = (
        ('Order Details', {
            'fields': ('order_number', 'date', 'stripe_payment_id',
                       'user_profile', 'status', 'price_total',
                       'shipping_total', 'grand_total',)
        }),
        ('Customer Info', {
            'fields': ('full_name', 'email', 'phone_number',)
        }),
        ('Gift message', {
            'fields': ('gift_message',)
        }),
        ('Payment Details', {
            'fields': ('payment_street_address1',
                       'payment_street_address2',
                       'payment_town_or_city',
                       'payment_county', 'payment_postcode',
                       'payment_country')
        }),
        ('Shipping Details', {
            'fields': ('shipping_full_name',
                       'shipping_street_address1',
                       'shipping_street_address2',
                       'shipping_town_or_city',
                       'shipping_county', 'shipping_postcode',
                       'shipping_country')
        }),
    )


admin.site.register(Order, OrderAdmin)
