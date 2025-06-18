from django.contrib import admin
from django.db import models
from django.conf import settings
from uuid import uuid4

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Collections(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True)
    #override method called __str__ like magic method
    def __str__(self):
        return self.title
    # ordering collections
    class Meta:
        ordering = ['title']
       
class Product(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField()
    slug = models.SlugField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collections, on_delete=models.PROTECT, related_name='products')
    promotions=models.ManyToManyField(Promotion)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
class Customer(models.Model):
    MEMBERSHIP_CHOICE_BRONZE='B'
    MEMBERSHIP_CHOICE_SILVER='S'
    MEMBERSHIP_CHOICE_GOLD='G'
    MEMBERSHIP_CHOICE=[
        (MEMBERSHIP_CHOICE_BRONZE,'bronze'),
        (MEMBERSHIP_CHOICE_SILVER,'silver'),
        (MEMBERSHIP_CHOICE_GOLD,'gold')
    ]
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICE,default=MEMBERSHIP_CHOICE_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    class Meta:
        ordering = ['user__first_name','user__last_name']
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key=True)

class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    class Meta:
        unique_together=[['cart','product']] # avoid making duplicate class product , just increase the quantity 
    @property
    def unit_price(self):
        return self.product.unit_price 
class Reviews(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=255)
    description=models.TextField()
    date = models.DateField(auto_now_add=True)
