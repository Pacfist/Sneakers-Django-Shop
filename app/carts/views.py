from django.shortcuts import render,get_object_or_404,redirect,reverse
from goods.models import Products
from carts.models import Cart
from django.http import HttpResponseRedirect
from django.contrib import auth,messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.utils import get_user_carts
from django.http import JsonResponse
from django.views import View
from carts.mixins import CartMixin
# Create your views here.

from django.contrib import messages

from django.contrib import messages
from django.template.loader import render_to_string


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Products, id=product_id)

        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity+=1
            cart.save()
        else:
            
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)
            
        response_data = {
            "message": "Товар добавлен в корзину",
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


# def cart_add(request):
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
        
#         product = get_object_or_404(Products, id=product_id)

#         if request.user.is_authenticated:
#             cart, created = Cart.objects.get_or_create(user=request.user, product=product)

#             if created:
#             # Set initial quantity to 1 when the item is newly added
#                 cart.quantity = 1
#                 messages.success(request, f"{product.name} was added to your cart.")
#             else:
#             # If the product is already in the cart, increment the quantity
#                 cart.quantity += 1
#                 messages.success(request, f"Updated {product.name} quantity in your cart.")

#             cart.save()
#         else:
#             carts = Cart.objects.filter(
#                 session_key=request.session.session_key,product=product
#             )
#             print(carts)
#             if carts.exists():
#                 cart=carts.first()
#                 if cart:
#                     cart.quantity+=1
#                     cart.save()
#             else:
#                 Cart.objects.create(
#                      session_key=request.session.session_key,product=product,quantity=1
#                 )

#         # Get the updated cart total quantity
#         total_quantity = Cart.objects.filter(user=request.user).total_quantity()

#         # Render the updated cart HTML
#         user_cart = get_user_carts(request)
#         cart_items_html = render_to_string(
#             "carts/includes/included_cart.html",
#             {"carts": user_cart},
#             request=request
#         )

#         # Render the messages HTML
#         messages_html = render_to_string('includes/notifications.html', {}, request=request)

#         # Return the response data, including the total quantity, cart HTML, and messages HTML
#         response_data = {
#             "cart_items_html": cart_items_html,
#             "qty": total_quantity,
#             "messages_html": messages_html,  # Include the rendered messages
#         }

#         return JsonResponse(response_data)









def cart_change(request,product_slug):
    return 0


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


# def cart_remove(request):

#     #cart = get_object_or_404(Cart, id=cart_id)
#     #cart.delete()
#     #return redirect(request.META['HTTP_REFERER'])


#     print("_________CART_REMOVE_______")
    
#     if request.POST.get('action') == 'post':
#         print("_________ACTION=POST_______")
#         product_id = int(request.POST.get('product_id'))
#         print("___________________PRODUCT_ID=",product_id,"__________________")
        
#         cart = get_object_or_404(Cart, id=product_id)
#         print("___________________CART=",cart,"__________________")

#         # Check if the product is already in the cart
#         cart.delete()

#         # Get the updated cart total quantity
#         total_quantity = Cart.objects.filter(user=request.user).total_quantity()

#         # Render the updated cart HTML
#         user_cart = get_user_carts(request)
#         cart_items_html = render_to_string(
#             "carts/includes/included_cart.html",
#             {"carts": user_cart},
#             request=request
#         )

#         # Render the messages HTML
#         messages_html = render_to_string('includes/notifications.html', {}, request=request)

#         # Return the response data, including the total quantity, cart HTML, and messages HTML
#         response_data = {
#             "cart_items_html": cart_items_html,
#             "qty": total_quantity,
#             "messages_html": messages_html,  # Include the rendered messages
#         }
#         print("_________JSON_RESPONSE_______")

#         return JsonResponse(response_data)