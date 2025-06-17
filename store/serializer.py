from rest_framework import serializers
from .models import Product, Collections , Reviews, Cart, CartItem
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
    
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
