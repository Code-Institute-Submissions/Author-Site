from datetime import datetime
from django.db import models

from series.models import Series


class Product(models.Model):
    _TYPE_OF_PRODUCT = [
        ('hard_back_book', 'Hard Back Book'),
        ('paper_back_book', 'Paper Back Book'),
        ('e_book', 'E-Book'),
        ('audio_book', 'Audio Book'),
        ('merchandise', 'Merchandise'),
    ]

    # ALL PRODUCTS
    name = models.CharField(max_length=254)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, related_name='products')
    product_type = models.CharField(choices=_TYPE_OF_PRODUCT, max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField()
    description = models.TextField()
    shipping = models.DecimalField(max_digits=6, decimal_places=2)
    recommended_audience_age = models.IntegerField()

    # ALL BOOKS
    author = models.CharField(max_length=254, null=True, blank=True)
    publish_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    publisher = models.CharField(max_length=254, null=True, blank=True)
    isbn = models.CharField(max_length=254, null=True, blank=True)

    # PHYSICAL BOOKS & E-BOOKS
    page_count = models.IntegerField(null=True, blank=True)

    # AUDIO BOOKS
    run_time = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    narrator = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
