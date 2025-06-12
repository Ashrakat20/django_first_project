from django.urls import path 
from . import views 
#urlconf
urlpatterns = [
    path('products/',views.product_list),
    path('products/<int:id>/',views.product_detail)
]
