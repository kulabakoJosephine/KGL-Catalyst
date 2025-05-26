import django_filters
from .models import Stock

class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = ['item_name']
