
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('offer/', views.offer, name = 'offer'),
    path('order_created/', views.order_created, name = 'order_created'),
    path('add_item_ajax/', views.add_item_ajax, name = 'add_item_ajax'),
    path('delete_from_cart_ajax/', views.delete_from_cart_ajax, name = 'delete_from_cart_ajax'),
    path('update_cart_info_ajax/', views.update_cart_info_ajax, name = 'update_cart_info_ajax'),
    path('add_quantity_ajax/', views.add_quantity_ajax, name = 'add_quantity_ajax'),
    path('remove_quantity_ajax/', views.remove_quantity_ajax, name = 'remove_quantity_ajax'),
    path('check_in_cart_ajax/', views.check_in_cart_ajax, name = 'check_in_cart_ajax'),
    path('update_cart_total_ajax', views.update_cart_total_ajax, name = 'update_cart_total_ajax'),
    path('create_order_ajax', views.create_order_ajax, name = 'create_order_ajax'),
    path('process_promo_ajax', views.process_promo_ajax, name = 'process_promo_ajax'),
    path('remove_promo_ajax', views.remove_promo_ajax, name = 'remove_promo_ajax'), 
]
