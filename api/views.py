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
from users.views import generate_code

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

def check_account_exist(request): 
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_phone = request.GET['user_phone']
        user_exist = User.objects.filter(
            phone = user_phone,
        ).exists()
        return JsonResponse({
            'status': status,
            'user_exist': user_exist
        }, status = 200)

def auth_user(request): 
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_phone = request.GET['user_phone']
        user_password = request.GET['user_password']
        user = User.objects.filter(
            phone = user_phone
        )
        password_corrent = user[0].check_password_correct(user_password)
        if (password_corrent): 
            auth_status = True
            user = list(user.values())[0]
        else:
            auth_status = False 
            user = None
        return JsonResponse({
            'status': status,
            'auth_status': auth_status,
            'user': user,
        }, status = 200)

def register_user_request(request): 
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_name = request.GET['user_name']
        user_phone = request.GET['user_phone']
        user_password = request.GET['user_password']

        print('user name: ', user_name, '\n')
        print('user user_phone: ', user_phone, '\n')
        print('user_password : ', user_password, '\n')

        sms_code = generate_code()

        sms_send = True

        return JsonResponse({
            'status': status,
            'sms_send': sms_send,
            'sms_code': sms_code,
        }, status = 200)

def register_user_finish(request): 
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_name = request.GET['user_name']
        user_phone = request.GET['user_phone']
        user_password = request.GET['user_password']

        print('user name: ', user_name, '\n')
        print('user user_phone: ', user_phone, '\n')
        print('user_password : ', user_password, '\n')

        user = User(
            name = user_name,
            phone = user_phone,
            password = user_password,
        )
        user.save()
        user = User.objects.filter(
            phone = user_phone
        )
        user_registered = True
        user = list(user.values())[0]
        return JsonResponse({
            'status': status,
            'user_registered': user_registered,
            'user': user,
        }, status = 200)

def get_user_info(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_id = request.GET['user_id']
        user_id = int(user_id)
        user = User.objects.filter(
            id = user_id
        )
        user = list(user.values())[0]
        return JsonResponse({
            'status': status,
            'user': user,
        }, status = 200)

def get_user_orders(request):
    print('get user orders request get')
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = True
        user_id = request.GET['user_id']
        user_id = int(user_id)
        user = User.objects.get(
            id = user_id
        )
        response_orders = []
        orders = user.order_set.all().order_by('-created_at');
        for order in orders:
            order_items = order.item_set.all()
            order_items = list(order_items.values())
            date_display = order.created_at.strftime("%Y-%m-%d %H:%M")        
            current_order = {
                'id': order.id,
                'created_at': order.created_at,
                'date_display': date_display,
                'name': order.name,
                'phone': order.phone,
                'delivery': order.delivery,
                'address': order.address,
                'payment': order.payment,
                'bonus_gained': order.bonus_gained,
                'coupon': order.coupon,
                'status': order.status,
                'status_display': order.get_status_display(),
                'order_cost': order.get_order_cost(),
                'order_items': order_items,
            }
            response_orders.append(current_order)
        return JsonResponse({
            'status': status,
            'orders': response_orders,
        }, status = 200)


def get_user_addresses(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_id = request.GET['user_id']
        user_id = int(user_id)
        user = User.objects.get(
            id = user_id
        )
        addresses = user.address_set.all()
        addresses = list(addresses.values())
        return JsonResponse({
            'status': status,
            'addresses': addresses,
        }, status = 200)

def delete_user_address(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_id = request.GET['user_id']
        user_id = int(user_id)
        address_id = request.GET['address_id']
        address_id = int(address_id)
        user = User.objects.get(
            id = user_id
        )
        address = Address.objects.get(
            id = address_id
        )
        user.address_set.remove(address)
        address.delete()
        return JsonResponse({
            'status': status,
            # maybe return deleted: yes | no
        }, status = 200)

def create_user_address(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_id = request.GET['user_id']
        user_id = int(user_id)
        user = User.objects.get(
            id = user_id
        )
        city = request.GET['city']
        street = request.GET['street']
        house = request.GET['house']
        flat = request.GET['flat']
        new_address = Address(
            user = user,
            city = city,
            street = street,
            house = house,
            flat = flat,
        )
        new_address.save()
        return JsonResponse({
            'status': status,
            # maybe return saved: yes | no
        }, status = 200)

def change_user_password(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        user_id = request.GET['user_id']
        new_password = request.GET['password']
        user_id = int(user_id)
        user = User.objects.get(
            id = user_id
        )
        password_changed = True
        try:
            user.set_password(new_password)
            user.save()
        except: 
            password_changed = False

        return JsonResponse({
            'status': status,
            'password_changed': password_changed,
        }, status = 200)

