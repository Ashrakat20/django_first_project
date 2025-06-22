from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action

from store.permissions import IsAdminOrReadOnly
from .models import Product, Collections, Reviews, Cart, CartItem, Customer
from .serializer import (
    ProductSerializer,
    CollectionsSerializer,
    ReviewsSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer,
)
from .filters import ProductFilter
from .pagination import DefaultPagination 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =  [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class=DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']  
    ordering_fields =['unit_price','last_update']
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         return queryset.filter(collection_id=collection_id)
    #     return queryset
    def get_serializer_context(self):
        return {'request': self.request}
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.exists():
            return Response(
                {'error': 'Product is associated with an order and cannot be deleted.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
        queryset = Collections.objects.annotate(product_count=Count('products')).all()
        serializer_class = CollectionsSerializer
        permission_classes = [IsAdminOrReadOnly]
        def get_serializer_context(self):
             return  {'request':self.request}
        def delete(self, request,pk):
            collection = get_object_or_404(Collections, pk=pk)

            if collection.product_set.exists():  # check if products exist in the collection
                return Response(
                    {'error': 'Cannot delete a collection with associated products.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )

            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class ReviewsViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
 
class CartViewSet(CreateModelMixin,
                  GenericViewSet,
                  RetrieveModelMixin,
                  DestroyModelMixin):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer
class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method =='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return{'cart_id': self.kwargs['cart_pk']}
    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == ['GET']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'],permission_classes = [IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)