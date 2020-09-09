from django.shortcuts import get_object_or_404

from .constants import ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL
from products.models import Product


def shopping_basket(request):
    """
    Context processor which provides access to the
    shopping basket content and custom message level.
    """
    # Placeholder variables
    no_of_products = 0
    products = []
    total_cost = 0
    shipping_cost = 0
    grand_total = 0

    # Load or create basket
    shopping_basket = request.session.get('shopping_basket', {})

    for product_id, amount in shopping_basket.items():

        # Get product
        product = get_object_or_404(Product, pk=product_id)

        # calculating subtotal
        subtotal = product.price * amount

        # Calculate placeholder variables
        no_of_products += amount
        total_cost += subtotal
        shipping_cost += product.shipping * amount
        grand_total += (subtotal + (product.shipping * amount))

        products.append({
            'product': product,
            'amount': amount,
            'subtotal': subtotal,
        })

    # TODO: sort products

    context =  {
        'ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL': ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL,
        'shopping_basket': {
            'no_of_products': no_of_products,
            'products': products,
            'total_cost': total_cost,
            'shipping_cost': shipping_cost,
            'grand_total': grand_total,
        }
    }

    return context
