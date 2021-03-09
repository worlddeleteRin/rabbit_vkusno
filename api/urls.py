
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [
    # api requests here,
    path('get_products', views.api_get_allproducts, name='api_get_allproducts'),
    path('get_categories', views.api_get_allcategories, name='api_get_allcategories'),
    path('get_stocks', views.get_stocks, name='get_stocks'),
]