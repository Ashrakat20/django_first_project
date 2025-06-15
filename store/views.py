from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product ,OrderItem , Collections
from .serializer import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializer import ProductSerializer ,CollectionsSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if product.orderitem_set.exists():
            return Response(
                {'error': 'Product is associated with an order and cannot be deleted.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        query_set = Collections.objects.all()
        serializer = CollectionsSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionsSerializer(data =request.data , context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
