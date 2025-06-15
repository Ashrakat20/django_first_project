from rest_framework import serializers
from .models import Product, Collections
from decimal import Decimal



class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Collections
        fields = ['id','title']
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ['id','title','unit_price','unit_price_with_tax','collection']
    
    unit_price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.HyperlinkedRelatedField(
          queryset= Collections.objects.all(),
          view_name= 'collection_detail'
      )
    def calculate_tax(self, product):
         return product.unit_price*Decimal(1.1)