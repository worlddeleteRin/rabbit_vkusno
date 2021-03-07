from django.shortcuts import render
from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
import urllib
import os
from django.core.files.storage import default_storage
from food_fabrik.settings import * 

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, reverse
import random

from twilio_sms import twilio_send_sms

from cart.models import * 
from products.models import * 
from users.models import * 

# Create your views here.

# api here

def api_get_allproducts(request):
    products = Product.objects.all()
    products = list(products.values())
    status = 'success'
    return JsonResponse({
        'status': status,
        'products': products,
    }, status = 200)

def api_get_allcategories(request):
    categories = Category.objects.all()
    categories = list(categories.values())
    status = 'success'
    return JsonResponse({
        'status': status,
        'categories': categories,
    }, status = 200)
    

