from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin , CreateModelMixin
from rest_framework.generics import ListCreateAPIView
from .models import Product  , Collections
from .serializer import ProductSerializer ,CollectionsSerializer


class Product_List(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
   
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.exists():
            return Response(
                {'error': 'Product is associated with an order and cannot be deleted.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
        queryset = Collections.objects.annotate(product_count=Count('products')).all()
        serializer_class = CollectionsSerializer
        def get_serializer_context(self):
             return {'request':self.request}

    
@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(Collections, pk=pk)

    if request.method == 'GET':
        serializer = CollectionsSerializer(collection, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollectionsSerializer(collection, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if collection.product_set.exists():
            return Response(
                {'error': 'Product is associated with an order and cannot be deleted.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
