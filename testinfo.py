import pandas as pd
import numpy as np

import os
import django
from django.conf import settings
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_fabrik.settings')
django.setup()

from users.models import * 
from cart.models import * 
from products.models import * 

TEST_USERS_COUNT = 90000
TEST_ORDERS_COUNT = 20

def generate():
    cart_items = []
    products_to_cart = Product.objects.all()[:5]
    for product in products_to_cart:
        item = Item(
            pr_id = product.id,
            name = product.name,
            price = product.price,
            sale_price = product.sale_price,
            category = product.category,
            quantity = 2,
            imgsrc = product.imgsrc
        )
        item.save()
        cart_items.append(item)
    print('-'*50)
    print('start generate')
    print('-'*50)
    for i in range (0, TEST_USERS_COUNT):
        phone = random.randint(71111111111, 79999999999)
        password = 343845
        name = 'somename_' + str(i)
        print('creating {} user...'.format(i))
        user = User(
            phone = phone,
            password = password,
            name = name,
        )
        user.save()
        print('user saved.')
        print('-'*50)
        print('start creating orders for user...')
        for i in range(TEST_ORDERS_COUNT): 
            order = Order(
                user = user,
                name = user.name,
                phone = user.phone,
                delivery = 'samovivoz',
                address = 'some address here',
                payment = 'payment is here',
                bonus_gained = 40
            )
            order.save()
            for item in cart_items:
                order.item_set.add(item)
        print(i, 'users generated', TEST_USERS_COUNT - i, 'left.')
    print('-'*50)

if __name__ == "__main__":
    generate()