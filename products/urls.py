
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:cat_id>', views.category, name = 'category'),
    path('<int:cat_id>/<int:dest_id>', views.destination, name = 'destination'),
    path('product/<int:product_id>', views.product, name = 'product'),
    path('stock/', views.stock, name = 'stock'),
]
