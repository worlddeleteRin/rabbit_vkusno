from django.shortcuts import render
from .models import * 
from django.http import JsonResponse, HttpResponse
import urllib
import os
from django.core.files.storage import default_storage
from food_fabrik.settings import * 
from cart.models import * 
from cart.views import get_or_create_cart

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, reverse
import random

from twilio_sms import twilio_send_sms


# Create your views here.



def index(request):
    authorized = is_authorized(request)
    if authorized:
        return redirect(reverse('users:orders'))
    else: 
        return redirect(reverse('users:login'))

def login(request):
    cart = get_or_create_cart(request)
    template  = 'users/login.html'
    context = {
        'cart': cart,
    }
    return render(request, template, context)
def register(request):
    cart = get_or_create_cart(request)
    template  = 'users/register.html'
    context = {
        'cart': cart,
    }
    return render(request, template, context)
def address(request):
    cart = get_or_create_cart(request)
    authorized = is_authorized(request)
    if authorized:
        user = get_user(request)
    else:
        user = None
    template  = 'users/address.html'
    context = {
        'user': user,
        'cart': cart,
    }
    return render(request, template, context)
def promo(request):
    cart = get_or_create_cart(request)
    authorized = is_authorized(request)
    if authorized:
        user = get_user(request)
    else:
        user = None
    template  = 'users/promo.html'
    context = {
        'user': user,
        'cart': cart,
    }
    return render(request, template, context)
def settings(request):
    cart = get_or_create_cart(request)
    authorized = is_authorized(request)
    if authorized:
        user = get_user(request)
    else:
        user = None
    template  = 'users/settings.html'
    context = {
        'cart': cart,
        'user': user,
    }
    return render(request, template, context)

def orders(request):
    cart = get_or_create_cart(request)
    authorized = is_authorized(request)
    if authorized:
        user = get_user(request)
    else:
        user = None
    if user == None:
        login_out_user(request)
        return redirect(reverse('users:login'))
    template = 'users/orders.html'
    user_orders = user.order_set.all().order_by('-created_at')
    context = {
        'cart': cart,
        'request': request,
        'authorized': authorized,
        'user': user,
        'user_orders': user_orders,
    }
    return render(request, template, context)

def order_item(request, order_id):
    cart = get_or_create_cart(request)
    authorized = is_authorized(request)
    if authorized:
        user = get_user(request)
    else:
        user = None
    order = Order.objects.get(id = order_id)
    template = 'users/order_item.html'
    context = {
        'request': request,
        'authorized': authorized,
        'user': user,
        'order': order,
        'cart': cart,
    }
    return render(request, template, context)

def restore(request):
    template = 'users/restore.html'
    context = {

    }
    return render(request, template, context)

def restore_ajax(request):
    msg = ''
    username = request.GET['username']
    rtype = request.GET['type']
    if rtype == 'check_account':
        if not (exist_user(username)):
            success = False
            msg = 'Пользователь с таким номером не зарегистрирован'
        else:
            success = True
            sms_code, status = send_code(username)
            request.session['sms_code'] = sms_code
    if rtype == 'verify_restore':
        return verify_user_restore(request)
    return JsonResponse({
        'success': success,
        'message': msg,
    },status = 200)

def login_ajax(request):
    print('start login ajax')
    success = False
    msg = ''
    username = request.GET['username']
    password = request.GET['password']
    user = auth_user(username, password)
    if user != None:
        login_user(request, user)
        msg = 'Вы авторизованы'
        success = True
    else:
        msg = 'Неверное имя пользователя или пароль'
    return JsonResponse({
        'message': msg,
        'success': success,
    },status = 200)

def login_out_ajax(request):
    print('start login out ajax')
    login_out_user(request)
    msg = 'your are logged out'
    return JsonResponse({
        'message': msg
    },status = 200)

def register_ajax(request):
    print('start register ajax')
    success = False
    msg = ''
    name = request.GET['name']
    username = request.GET['username']
    password = request.GET['password']
    rtype = request.GET['type']
    if rtype == 'check_account':
        return check_user_account(request, username)
    if rtype == 'verify_account':
        return verify_user_account(request)

def check_user_account(request, username):
    msg=''
    user_exist = exist_user(username)
    if user_exist:
        success = False
        msg = 'На данный номер телефона уже создан аккаунт. Пожалуйста, авторизуйтесь'
    else:
        success = True
        code, result = send_code(username)
        print(result)
        request.session['sms_code'] = code
    # # user = auth_user(username, password)
    # if user != None:
    #     login_user(request, user)
    #     msg = 'Вы авторизованы'
    #     success = True
    # else:
    #     msg = 'Неверное имя пользователя или пароль'
    return JsonResponse({
        'message': msg,
        'success': success,
    },status = 200)

def verify_user_restore(request):
    msg = ''
    username = request.GET['username']
    user_code = request.GET['user_code']
    sms_code = request.session['sms_code']
    print('user code: ', user_code)
    print('sms code: ', sms_code)
    if int(user_code) == int(sms_code):
        print('user code pass')
        success = True
        user = User.objects.get(phone = username)
        login_user(request, user)
    else:
        success = False
        msg = 'Неверный код!'
    return JsonResponse({
        'success': success,
        'message': msg,
    }, status = 200)

def verify_user_account(request):
    msg = ''
    name = request.GET['name']
    username = request.GET['username']
    password = request.GET['password']
    user_code = request.GET['user_code']
    sms_code = request.session['sms_code']
    print('user code: ', user_code)
    print('sms code: ', sms_code)
    if int(user_code) == int(sms_code):
        print('user code pass')
        success = True
        user = register_user(name, username, password)
        login_user(request, user)
    else:
        success = False
        msg = 'Неверный код!'
    return JsonResponse({
        'success': success,
        'message': msg,
    }, status = 200)

def change_password_ajax(request):
    new_password = request.GET['password']
    user = get_user(request)
    if user != None:
        user.password = new_password
        user.save()
        success = True
    else:
        success = False
    return JsonResponse({
        'success': success,
    }, status = 200)


def send_code(username):
    print('start to send code')
    auth_code = generate_code()
    result = twilio_send_sms(auth_code, username)
    return auth_code, result

def generate_code(): 
    code = random.randint(125916, 986921)
    return code

def address_action_ajax(request):
    user = get_user(request)

    action = request.GET['action']

    if action != 'delete':
        city = request.GET['city']
        street = request.GET['street']
        house = request.GET['house']
        flat = request.GET['flat']
        comment = request.GET['comment']

    success = True
    
    if action == 'add':
        address = Address(
            user = user,
            city = city,
            street = street,
            house = house,
            flat = flat,
            comment = comment,
        )
        address.save()
        need_render = request.GET['need_render']
        if (need_render == 'true'):
            user = get_user(request)
            template = 'cart/blocks/offer_address_block.html'
            context = {
                'user': user
            }
            return render(request, template, context)
    if action == 'edit':
        address_id = request.GET['address_id']
        address = Address.objects.get(
            id = address_id
        )
        address.city = city
        address.street = street
        address.house = house
        address.flat = flat
        address.comment = comment
        address.save()
    if action == 'delete':
        address_id = request.GET['address_id']
        address = Address.objects.get(
            id = address_id
        )
        address.delete()
    return JsonResponse({
        'success': success
    }, status = 200)

