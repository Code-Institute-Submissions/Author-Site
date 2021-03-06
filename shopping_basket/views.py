from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product
from .constants import ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL


def view_or_update_shopping_basket(request):
    """ A view to return the shopping basket page """

    if request.method == 'POST':
        product_id = request.POST['product_id']
        amount = int(request.POST['amount'])
        shopping_basket = request.session.get('shopping_basket', {})

        shopping_basket[product_id] = amount

        # Delete item
        if shopping_basket[product_id] < 1:
            del shopping_basket[product_id]

        # Prevent amount over 99
        elif shopping_basket[product_id] > 99:
            messages.warning(
                request,
                'The maximum number of products you can purchase at \
                any one time is 99. If you wish to make a larger \
                purchase (for schools etc) please contact us directly!')
            shopping_basket[product_id] = 99

        request.session['shopping_basket'] = shopping_basket

    return render(request, 'shopping_basket/shopping_basket.html')


def add_to_shopping_basket(request, product_id):
    """ A view to add items to the user's shopping basket """

    # Check product exists
    product = get_object_or_404(Product, pk=product_id)

    # Redirect info
    redirect_url = request.POST.get('redirect_url')

    # Check product is in stock
    if not product.in_stock:
        messages.warning(request,
            " I'm sorry, this product is currently out of stock. \
            Once our suppliers give us the thumbs up it will be \
            back though, so check back soon!"
        )
        return redirect(redirect_url)

    # Load or create basket
    shopping_basket = request.session.get('shopping_basket', {})

    # Add to the shopping basket with custom sucess messages for the customer
    if product_id in shopping_basket:
        shopping_basket[product_id] += 1

        if product.product_type == 'merchandise':
            messages.add_message(
                request,
                ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL,
                f'Hey, you just added another { product.name } to your shopping basket!')
        else:
            messages.add_message(
                request,
                ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL,
                f'Hey, you just added another { product.get_product_type_display() } version of { product.name } to your shopping basket!')
    else:
        shopping_basket[product_id] = 1

        if product.product_type == 'merchandise':
            messages.add_message(
                request,
                ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL,
                f'Hey, you just added a { product.name } to your shopping basket!')
        elif product.product_type in ['audio_book', 'e_book']:
            messages.add_message(
                request,
                ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL,
                f'Hey, you just added an { product.get_product_type_display() } version of { product.name } to your shopping basket!')
        else:
            messages.add_message(
                request,
                ADD_TO_SHOPPING_BASKET_MESSAGE_LEVEL,
                f'Hey, you just added a { product.get_product_type_display() } version of { product.name } to your shopping basket!')

    request.session['shopping_basket'] = shopping_basket

    return redirect(redirect_url)
