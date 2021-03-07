import pandas as pd
import numpy as np

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_fabrik.settings')
django.setup()

from products.models import * 


def create_products():
    deleteall()
    path ='/Users/noname/work/ffabrik/host/goods_main.csv'
    data = pd.read_csv(path)
    print('data is ', len(data))
    for index, item in data.iterrows():
        print('start creating product')
        cat = Category.objects.get_or_create(
            slug = item['category'],
            name = item['category'],
            imgsrc = 'static/images/products/' + item['category_img']
        )[0]
        # print('current category', cat)
        if np.isnan(item['sale_price']):
            sale_price = 0
        else:
            sale_price = item['sale_price']
        product = Product(
            category = cat,
            name = item['name'],
            price = item['price'],
            sale_price = sale_price,
            ves = item['ves'],
            description = item['description'],
            imgsrc = 'static/images/products/' + item['imgsrc'],
        )
        product.save()

if __name__ == "__main__":
    create_products()