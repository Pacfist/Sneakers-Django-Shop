from django.shortcuts import render,get_object_or_404,redirect,reverse
from goods.models import Products
from carts.models import Cart
from django.http import HttpResponseRedirect
from django.contrib import auth,messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.utils import get_user_carts
from django.http import JsonResponse

# Create your views here.

from django.contrib import messages

from django.contrib import messages
from django.template.loader import render_to_string

def cart_add(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        product = get_object_or_404(Products, id=product_id)

        # Check if the product is already in the cart
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)

        if created:
            # Set initial quantity to 1 when the item is newly added
            cart.quantity = 1
            messages.success(request, f"{product.name} was added to your cart.")
        else:
            # If the product is already in the cart, increment the quantity
            cart.quantity += 1
            messages.success(request, f"Updated {product.name} quantity in your cart.")

        cart.save()

        # Get the updated cart total quantity
        total_quantity = Cart.objects.filter(user=request.user).total_quantity()

        # Render the updated cart HTML
        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/includes/included_cart.html",
            {"carts": user_cart},
            request=request
        )

        # Render the messages HTML
        messages_html = render_to_string('includes/notifications.html', {}, request=request)

        # Return the response data, including the total quantity, cart HTML, and messages HTML
        response_data = {
            "cart_items_html": cart_items_html,
            "qty": total_quantity,
            "messages_html": messages_html,  # Include the rendered messages
        }

        return JsonResponse(response_data)









def cart_change(request,product_slug):
    return 0



def cart_remove(request):

    #cart = get_object_or_404(Cart, id=cart_id)
    #cart.delete()
    #return redirect(request.META['HTTP_REFERER'])
    product_id = int(request.POST.get('product_id'))
    
    cart = get_object_or_404(Cart, id=product_id)
    print(cart)
        # Check if the product is already in the cart
    cart.delete()

        # Get the updated cart total quantity
    total_quantity = Cart.objects.filter(user=request.user).total_quantity()

        # Render the updated cart HTML
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html",
        {"carts": user_cart},
        request=request
    )

        # Render the messages HTML
    messages_html = render_to_string('includes/notifications.html', {}, request=request)

        # Return the response data, including the total quantity, cart HTML, and messages HTML
    response_data = {
        "cart_items_html": cart_items_html,
        "qty": total_quantity,
        "messages_html": messages_html,  # Include the rendered messages
    }

    return JsonResponse(response_data)