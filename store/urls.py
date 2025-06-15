from django.urls import path 
from rest_framework.routers import DefaultRouter
from . import views 
from pprint import pprint
#urlconf
router=DefaultRouter()
router.register('products',views.ProductViewSet,basename='product')
router.register('collections',views.CollectionViewSet,basename='collection')
urlpatterns = router.urls

# urlpatterns = [
#     path('products/',views.ProductList.as_view()),
#     path('products/<int:pk>/',views.ProductDetail.as_view()),
#     path('collections/<int:pk>/',views.CollectionDetail.as_view()),
#     path('collections/',views.CollectionList.as_view())
# ]
