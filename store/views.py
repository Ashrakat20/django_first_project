from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializer import ProductSerializer
# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':  # <-- FIXED: 'POST' in uppercase
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # You might want to save the data here
        return Response('ok')
        
        
@api_view(['GET','PUT'])
def product_detail(request,id):
    """ Note: we moved product instance outside cause we need to use a product instance while 
    updating object 
    """
    product =get_object_or_404(Product,  pk=id)
    if request.method == 'GET':
        serializer= ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # You might want to save the data here
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view()
def collection_detail(request,pk):
        return Response('ok')