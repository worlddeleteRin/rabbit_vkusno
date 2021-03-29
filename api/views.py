from django.shortcuts import render
from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
import urllib
import os
import json

from django.core.files.storage import default_storage
from food_fabrik.settings import * 
from food_fabrik.critical_variables import * 

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, reverse
import random
import ast

from twilio_sms import twilio_send_sms

from cart.models import * 
from products.models import * 
from users.models import * 

from .models import * 
from users.views import generate_code


# from django.core import serializers



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
        products = Product.objects.all().order_by('-price').order_by('display_priority')
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
        categories = Category.objects.all().order_by('display_priority')
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
        stocks = Stock.objects.all().order_by('-display_priority')
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
        print('phone is ', user_phone)
        twilio_response = twilio_send_sms(sms_code, user_phone)
        print(twilio_response)

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
            # pack orders items
            order_items_list = []
            for order_item in order_items:
                current_item = {
                    'id': order_item.id,
                    'quantity': order_item.quantity,
                    'name': order_item.product.name,
                    'category_id': order_item.product.category.id,
                    'price': order_item.product.price,
                    'sale_price': order_item.product.sale_price,
                    'imgsrc': order_item.product.imgsrc.name,
                }
                order_items_list.append(current_item)

            # order_items = list(order_items.values())
            print('order items are', order_items_list)
            date_display = order.created_at.strftime("%Y-%m-%d %H:%M")
            if (order.coupon):
                order_coupon = order.coupon.code
            else:
                order_coupon = None        
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
                'coupon': order_coupon,
                'status': order.status,
                'status_display': order.get_status_display(),
                # 'order_cost': order.get_order_cost(),
                'order_cost': order.amount,
                'order_items': order_items_list,
                'purchase_amount': order.amount,
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

def create_order_not_auth(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'

        # get necessary data
        delivery_method = request.GET['delivery_method']
        payment_method = request.GET['payment_method']
        order_address = request.GET['order_address']
        user_name = request.GET['user_name']
        user_phone = request.GET['user_phone']

        cart_items = json.loads(request.body)['cart_items']
        purchase_amount = json.loads(request.body)['purchase_amount']
        delivery_discount_use = json.loads(request.body)['delivery_discount_use']

        if int(delivery_method) == 1:
            delivery = 'Доставка'
        else:
            delivery = 'Самовывоз'
        if int(payment_method) == 1:
            payment = 'Наличные'
        else:
            payment = 'Картой курьеру'

        # start creating an order
        new_order = Order(
            amount = purchase_amount,
            name = user_name,
            phone = user_phone,
            delivery = delivery,
            address = order_address,
            payment = payment,
            delivery_discount_use = delivery_discount_use,
        )
        new_order.save()
        for item in cart_items:
            product = Product.objects.get(id = item['id'])
            new_item = Item(
                product = product,
                quantity = item['quantity'],
            )
            new_item.save()
            new_order.item_set.add(new_item)
        # print('cart items are', cart_items)
        # print('purchase amount is', purchase_amount)

        return JsonResponse({
            'status': status,
            'order_created': True,
        }, status = 200)

def create_order_auth(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'

        # get necessary data
        user_id = int(request.GET['user_id'])
        delivery_method = request.GET['delivery_method']
        payment_method = request.GET['payment_method']
        order_address_id = int(request.GET['order_address_id'])

        cart_items = json.loads(request.body)['cart_items']
        purchase_amount = json.loads(request.body)['purchase_amount']
        promo_used = json.loads(request.body)['promo_used']
        delivery_discount_use = json.loads(request.body)['delivery_discount_use']
        if not promo_used:
            promo_used = None
        else:
            promo_used = Coupon.objects.get(id = promo_used['id'])

        # get current user
        current_user = User.objects.get(id = user_id)

        if int(delivery_method) == 1:
            delivery = 'Доставка'
            address = Address.objects.get(id = order_address_id).get_full()
        else:
            delivery = 'Самовывоз'
            address = ''
        if int(payment_method) == 1:
            payment = 'Наличные'
        else:
            payment = 'Картой курьеру'

        bonus_gained = calc_bonus_gained(current_user, purchase_amount)

        # start creating an order
        new_order = Order(
            user = current_user,
            amount = purchase_amount,
            name = current_user.name,
            phone = current_user.phone,
            delivery = delivery,
            address = address,
            payment = payment,
            bonus_gained = bonus_gained,
            coupon = promo_used,
            delivery_discount_use = delivery_discount_use,
        )
        new_order.save()
        for item in cart_items:
            product = Product.objects.get(id = item['id'])
            new_item = Item(
                product = product,
                quantity = item['quantity'],
            )
            new_item.save()
            new_order.item_set.add(new_item)
        # print('cart items are', cart_items)
        # print('purchase amount is', purchase_amount)

        return JsonResponse({
            'status': status,
            'order_created': True,
        }, status = 200)

def check_promo(request):
    print('got check promo request')
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        promo_code = request.GET['promo_code']
        promo_exist = Coupon.objects.filter(
            code = promo_code
        ).exists()
        if (promo_exist):
            promo = Coupon.objects.get(
                code = promo_code
            )
            promo_categories = list(promo.categories.all().values())
            promo_products = list(promo.products.all().values())
            response_promo = {
                'id': promo.id,
                'code': promo.code,
                'discount': promo.discount,
                'valid_from': promo.valid_from,
                'valid_to': promo.valid_to,
                'usage_type': promo.usage_type,
                'active': promo.active,
                'from_amount': promo.from_amount,
                'promo_categories': promo_categories,
                'promo_products': promo_products,
            }
            return JsonResponse({
            'promo_status': True,
            'promo': response_promo,
            }, status = 200)
        else:
            return JsonResponse({
            'promo_status': False,
            'msg': 'Введенный промокод не найден',
            }, status = 200)


def get_critical_info(request):
    authorized = api_authorize(request)
    if not authorized:
        return return_401()
    else:
        status = 'success'
        return JsonResponse({
        'status': status,
        'delivery_byclient_discount': DELIVERY_BYCLIENT_DISCOUNT,
        'delivery_byclient_address': DELIVERY_BYCLIENT_ADDRESS,
        'delivery_phone': DELIVERY_PHONE,
        'delivery_address_map': DELIVERY_ADDRESS_MAP,
        }, status = 200)