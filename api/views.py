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

from .models import * 

# Create your views here.

# api here
def api_authorize(request):
    status = True
    try:
        access_token = request.GET['access_token']
        token_exist = AccessToken.objects.filter(
            token = access_token
        ).exists()
        if not token_exist:
            status = False
        else:
            status = True
    except:
        status = False
    return status
def return_401():
    return JsonResponse({
        'status': 'error',
        'msg': 'no access token provided or access token invalid'
    }, status = 200)

# api endpoints

def api_get_allproducts(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        products = Product.objects.all()
        products = list(products.values())
        status = 'success'
        return JsonResponse({
            'status': status,
            'products': products,
        }, status = 200)

def api_get_allcategories(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        categories = Category.objects.all()
        categories = list(categories.values())
        status = 'success'
        return JsonResponse({
            'status': status,
            'categories': categories,
        }, status = 200)
    
def get_stocks(request): 
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        stocks = Stock.objects.all()
        stocks = list(stocks.values())
        status = 'success'
        return JsonResponse({
            'status': status,
            'stocks': stocks,
        }, status = 200)
