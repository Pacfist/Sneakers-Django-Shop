from django import template 
from carts.models import Cart
from carts.utils import get_user_carts
register=template.Library()

@register.simple_tag()
def user_carts(request):
    cart = request.session.get("carts", {})
    
    return cart

@register.simple_tag()
def user_carts_total(request):
    cart = request.session.get("carts", {})
    total_price = 0
    total_quantity = 0
    for key,item in cart.items():
        total_price += item['price'] * item['quantity']
        total_quantity += item['quantity']

    total = {"total_price":total_price,"total_quantity":total_quantity }
    return total

