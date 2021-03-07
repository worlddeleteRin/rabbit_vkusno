from django import template
from users.models import * 


register = template.Library()

@register.assignment_tag
def get_address_by_id(address_id):
    address = Address.objects.get(
        id = address_id
    )
    return address