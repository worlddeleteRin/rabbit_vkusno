
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [
    # api requests here,
    path('get_products', views.api_get_allproducts, name='api_get_allproducts'),
    path('get_categories', views.api_get_allcategories, name='api_get_allcategories'),
    path('get_stocks', views.get_stocks, name='get_stocks'),
    path('check_account_exist', views.check_account_exist, name='check_account_exist'),
    path('auth_user', views.auth_user, name='auth_user'),
    path('register_user_request', views.register_user_request, name='register_user_request'),
    path('register_user_finish', views.register_user_finish, name='register_user_finish'),
    path('get_user_info', views.get_user_info, name='get_user_info'),
]