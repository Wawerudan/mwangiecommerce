import django_filters
from .models import ProductVariant

class VariantFilter(django_filters.FilterSet):
    color = django_filters.CharFilter(field_name='color', lookup_expr='iexact')
    size = django_filters.CharFilter(field_name='size', lookup_expr='iexact')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = ProductVariant
        fields = ['color', 'size', 'min_price', 'max_price']
