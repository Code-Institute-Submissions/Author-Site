from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404


from .models import Product
from series.models import Series


def all_products(request):
    """ A view to return all products """

    products = Product.objects.all().filter(list_in_shop=True)

    # Variables for filtering
    selected_series = request.GET.get('series', '')
    selected_product_type = request.GET.get('product_type', '')

    series_list = Series.objects.all()
    product_types = Product._TYPE_OF_PRODUCT

    # Filtering code
    if selected_series != '':
        try:
            selected_series = int(selected_series)
            products = products.filter(series__id=selected_series)
        except ValueError:
            selected_series = ''

    if selected_product_type != '':
        try:
            products = products.filter(product_type=selected_product_type)
        except ValueError:
            selected_product_type = ''

    # Pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'current_page': 'products',
        'selected_series': selected_series,
        'series_list': series_list,
        'selected_product_type': selected_product_type,
        'product_types': product_types,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show an individual product """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'current_page': 'products',
    }

    return render(request, 'products/product_detail.html', context)
