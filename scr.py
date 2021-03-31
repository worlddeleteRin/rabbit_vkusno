import pandas as pd
import numpy as np

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_fabrik.settings')
django.setup()

from products.models import * 

PRODUCTS_PATH = '/Users/noname/work/fabrika_edi/main_project/goods/goods_main3.xlsx'


def create_products():
    deleteall()
    data = pd.read_excel(PRODUCTS_PATH)
    print('data is ', len(data))
    for index, item in data.iterrows():
        print('start creating product')
        print('product index is', index)
        print('product name is', item['name'])
        print('product category is', item['category'])
        cat_slug = str(item['category'].lower().strip())
        if not Category.objects.filter(slug = cat_slug).exists():
            cat = Category.objects.get_or_create(
                slug = cat_slug,
                name = item['category'],
                imgsrc = 'static/images/products/' + item['category_img'].strip(),
		display_priority = item['category_priority']
            )[0]
        else:
            cat = Category.objects.get(slug = cat_slug)
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
            imgsrc = 'static/images/products/' + item['imgsrc'].strip(),
	    display_priority = item['display_priority']
        )
        product.save()

if __name__ == "__main__":
    create_products()
