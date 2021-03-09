
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('orders/', views.orders, name = 'orders'),
    path('orders/<int:order_id>', views.order_item, name = 'order_item'),
    path('login_ajax', views.login_ajax, name = 'login_ajax'),
    path('login_out_ajax', views.login_out_ajax, name = 'login_out_ajax'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('settings', views.settings, name = 'settings'),
    path('address', views.address, name = 'address'),
    path('address_action_ajax', views.address_action_ajax, name = 'address_action_ajax'),
    path('promo', views.promo, name = 'promo'),
    path('restore', views.restore, name = 'restore'),
    path('register_ajax', views.register_ajax, name = 'register_ajax'),
    path('restore_ajax', views.restore_ajax, name = 'restore_ajax'),
    path('change_password_ajax', views.change_password_ajax, name = 'change_password_ajax'),
]
