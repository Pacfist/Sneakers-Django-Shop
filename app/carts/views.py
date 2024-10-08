from django.shortcuts import render,get_object_or_404,redirect,reverse
from goods.models import Products
from carts.models import Cart
from django.http import HttpResponseRedirect
from django.contrib import auth,messages
# Create your views here.

def cart_add(request, product_slug):
    
    product=get_object_or_404(Products, slug=product_slug)
    
    
    if request.user.is_authenticated:
       
        carts = Cart.objects.filter(user=request.user, product = product)
        
        if carts.exists():
            cart=carts.first()
            if cart:
                cart.quantity+=1
                cart.save()
        else:
             Cart.objects.create(user=request.user, product=product, quantity=1)   
     
    messages.success(request, f"{product.name}, added to the cart")
    return redirect(request.META['HTTP_REFERER'])




def cart_change(request,product_slug):
    return 0



def cart_remove(request,product_slug):
    return 0