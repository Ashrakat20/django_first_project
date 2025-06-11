from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Count , Max , Min
from django.db.models import Value , F, Min, Func
from store.models import Product , OrderItem, Order, Customer



def say_hello(request):
    queryset = Customer.objects.annotate(new_id=F('id'))
    return render(request, 'hello.html' , {'name':'Mosh','result': list(queryset)})
