from django import template

from products.models import *
from cart.models import * 
from users.models import * 

register = template.Library()


@register.simple_tag
def is_in_cart(product, cart):
    items = cart.item_set.all()
    exist = items.filter(
        cart = cart,
        product = product,
    ).exists()
    return exist
    
@register.simple_tag
def modify_imgsrc(imgsrc):
    img = imgsrc.url.replace('/static/images/products/', '')
    img = imgsrc.url.replace('static/images/products/', '')
    return '/static/images/products/' + img
    # return imgsrc.replace('static/', '')

@register.simple_tag
def modify_stock_desc(desc):
    if len(desc) > 100:
        return desc[:100] + ' ...'
    else:    
        return desc[:100]
        

@register.simple_tag
def get_address_by_id(address_id):
    address = Address.objects.get(
        id = address_id
    )
    return address







