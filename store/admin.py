from itertools import count 
from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

@admin.register(models.Product) # decorator for registering product model
class ProductAdmin(admin.ModelAdmin): #product admin class that inherits from model admin
    list_display=['title','unit_price','inventory_status','collection']
    list_editable =['unit_price']
    list_per_page = 10
    list_select_related=['collection']
    #computed column NOTE:important
    @admin.display(ordering='inventory')
    def inventory_status(self, Product):
        if Product.inventory <10:
            return 'Low'
        return 'Ok'



@admin.register(models.Collections)
class CollectionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']

    @admin.display(ordering='products_count')
    def product_count(self, collections):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collections.id)})
        )
        return format_html('<a href="{}">{} Products</a>', url, collections.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))



@admin.register(models.Customer) # decorator for registering customer model
class CustomerAdmin(admin.ModelAdmin): #customer admin class that inherits from model admin
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    list_per_page = 10
    list_filter = ('membership',)


@admin.register(models.Order) # decorator for registering Order model
class OrderAdmin(admin.ModelAdmin): #order admin class that inherits from model admin
    list_display=['id','placed_at','customer']
   