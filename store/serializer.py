from rest_framework import serializers
from .models import Product, Collections
from decimal import Decimal



class CollectionsSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collections
        fields = ['id', 'title', 'product_count']
        product_count = serializers.IntegerField(read_only=True)



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