from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Product  , Collections , Reviews
from .serializer import ProductSerializer ,CollectionsSerializer,ReviewsSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
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
        return {'request': self.request}
 