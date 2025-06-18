from itertools import count
from django.contrib import admin , messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

@admin.register(models.Product) # decorator for registering product model
class ProductAdmin(admin.ModelAdmin): #product admin class that inherits from model admin
    prepopulated_fields= {
        'slug': ['title']
    }
    autocomplete_fields=['collection']
    actions = ['clear_inventory']
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
    #custom action
    @admin.action(description='clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count}products was succesfully deleted ',
            messages.ERROR
        )


@admin.register(models.Collections)
class CollectionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields=['title']
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
    search_fields=['first_name','last_name']
    list_display=['first_name','last_name','membership','orders']
    list_editable=['membership']
    list_per_page = 10
    list_select_related =['user']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__startswith','last_name__startswith']
    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({'customer__id': str(customer.id)})
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))

class OrderItemInline(admin.TabularInline):
    autocomplete_fields=['product']
    model=models.OrderItem
    extra = 0
    min_num=1
    max_num=10

@admin.register(models.Order) # decorator for registering Order model
class OrderAdmin(admin.ModelAdmin): #order admin class that inherits from model admin
    list_display=['id','placed_at','customer']
    inlines=[OrderItemInline]
    autocomplete_fields=['customer']
