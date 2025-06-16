from rest_framework import serializers
from .models import Product, Collections , Reviews
from decimal import Decimal



class CollectionsSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collections
        fields = ['id', 'title', 'product_count']
        #product_count = serializers.IntegerField(read_only=True)



class ProductSerializer(serializers.ModelSerializer):
    unit_price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collections.objects.all(),
        view_name='collection-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'unit_price_with_tax', 'collection']

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)
    
    
class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ['id', 'name', 'description','date']
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Reviews.objects.create(product_id= product_id,**validated_data)     
