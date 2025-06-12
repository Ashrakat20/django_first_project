from rest_framework import serializers
from .models import Product, Collections
from decimal import Decimal


class CollectionsSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    
class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    Price =serializers.DecimalField(max_digits=6,decimal_places=2, source='unit_price')
    unit_price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.HyperlinkedRelatedField(
        queryset= Collections.objects.all(),
        view_name= 'collection_detail'
    )
    def calculate_tax(self, product):
        return product.unit_price*Decimal(1.1)