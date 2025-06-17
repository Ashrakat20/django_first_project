from django.urls import path 
from rest_framework_nested import routers
from . import views 
#urlconf
router=routers.DefaultRouter() # parent router 
router.register('products',views.ProductViewSet,basename='product')
router.register('collections',views.CollectionViewSet,basename='collection')
router.register('cart', views.CartViewSet, basename='cart')

products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewsViewSet,basename='product-reviews')


urlpatterns = router.urls + products_router.urls

# urlpatterns = [
#     path('products/',views.ProductList.as_view()),
#     path('products/<int:pk>/',views.ProductDetail.as_view()),
#     path('collections/<int:pk>/',views.CollectionDetail.as_view()),
#     path('collections/',views.CollectionList.as_view())
# ]
