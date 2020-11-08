
from django.shortcuts import render
from .models import * 
from django.http import JsonResponse, HttpResponse
import urllib
import os
from django.core.files.storage import default_storage
from food_fabrik.settings import * 
from cart.models import * 


# Create your views here.

def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def get_or_create_cart(request):
    session_key = get_session_key(request)
    current_cart = Cart.objects.get_or_create(
        session_key = session_key,
    )[0],
    return current_cart[0]



def index(request):
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    categories = Category.objects.all()
    # destinations = Destination.objects.all()
    products = Product.objects.all()
    sale_products = Product.objects.filter(
        sale_price__gte = 1
    )
    return render(request, 'products/index.html', {
        'categories': categories,
        'products': products,
        'session_key': session_key,
        'cart': cart,
        'sale_products': sale_products,
        # 'destinations': destinations,
    })
def product(request, product_id):
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    current_product = Product.objects.get(id = product_id)
    return render(request, 'products/product.html', {
        'product': current_product,
        'cart': cart,
        'session_key': session_key,
    })



def destination(request, cat_id, dest_id):
    session_key = get_session_key(request)
    current_cat = Category.objects.get(
        id = cat_id,
    )
    current_dest = Destination.objects.get(
        category = current_cat,
        id = dest_id,
    )
    products = current_dest.product_set.all()
    return render(request, 'products/dest.html', {
        'current_cat': current_cat,
        # 'current_dest': current_dest,
        'products': products,
    })

def category(request, cat_id):
    session_key = get_session_key(request)
    
    current_cat = Category.objects.get(
        id = cat_id,
    )
    
    products = Product.objects.filter(
        category = current_cat,
    )
    return render(request, 'products/category.html', {
        'current_cat': current_cat,
        # 'current_dest': current_dest,
        'products': products,
    })

def stock(request):
    session_key = get_session_key(request)
    cart = get_or_create_cart(request)
    stocks = Stock.objects.all()
    return render(request, 'products/stock.html', {
        'cart': cart,
        'stocks': stocks,
    })


