from django.urls import path 
from . import views 
#urlconf
urlpatterns = [
    path('products/',views.Product_List.as_view()),
    path('products/<int:id>/',views.ProductDetail.as_view()),
    path('collections/<int:pk>/',views.collection_detail,name='collection_detail'),
    path('collections/',views.CollectionList.as_view())
]
