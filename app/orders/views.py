from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from orders.forms import CreateOrderForm
from django.db import transaction
from carts.models import Cart
from orders.models import Order, OrderItem
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Products, ProductSizeQuantity
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from users.models import User
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

import json

class CreateCheckout(View):
    YOUR_DOMAIN = "http://127.0.0.1:8000/orders/"

    def post(self, request, *args, **kwargs):
        products = self.request.session.get("carts", {})
        print(products)
        itemList = []
        

        for key, item in products.items():
            # Use price_data to create prices dynamically
            print(int(item['price'] * 100))
            itemList.append({
                'price_data': {
                    'currency': 'cad',  # Use your currency
                    'unit_amount': int(item['price'] * 100),  # Convert to cents
                    'product_data': {
                        'name': item['product_name'],
                        'description': f"Size: {item['size_name']}",  # Add size in the product description
                    },
                },
                'quantity': int(item['quantity']),
            })

            # Append item details to metadata list
            
        
        try:
            # Create a Stripe Checkout Session with serialized item data in metadata
            checkout_session = stripe.checkout.Session.create(
                line_items=itemList,
                mode='payment',
                success_url=self.YOUR_DOMAIN + 'success/',
                cancel_url=self.YOUR_DOMAIN + 'cancel/',
                metadata={
                    'user': self.request.user.id , # Serialize the items list to JSON
                    'products': json.dumps(products), 
                },
                billing_address_collection='required',  # Collect billing address
                shipping_address_collection={           # Collect shipping address
                    'allowed_countries': ['US', 'CA'],  # Specify allowed countries
                },
                phone_number_collection={              # Collect phone number
                    'enabled': True                    # Enable mandatory phone number input
                },
            )

            # Redirect to the Stripe Checkout page
            return redirect(checkout_session.url, code=303)

        except Exception as e:
            # Handle any errors from Stripe
            return JsonResponse({'error': str(e)})



# Using Django
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print('Error parsing payload: {}'.format(str(e)))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('Error verifying webhook signature: {}'.format(str(e)))
        return HttpResponse(status=400)
    
   
    
    if event.type == 'checkout.session.completed':
        #payment_method = event.data.object 
        
        session = event['data']['object']
        user_id = session["metadata"]["user"]

        customer_email=session["customer_details"]["email"]
        body=""
        products = json.loads(session["metadata"]["products"])
        print(f"The products in web-hook ----------------------------\n{products}")

        body = ", ".join(item["product_name"] for item in products.values())


        body = body.strip(", ")
        send_mail(
            subject = "Here is yours product",
            message=f"Thanks for your purchasing the {body}",
            recipient_list=[customer_email],
            from_email=['test@test.com']
        )

        
        user = User.objects.get(id=user_id)
        customer_email = session["customer_details"]["email"]
        customer_name = session["customer_details"]["name"] 
        address = session["customer_details"]["address"]
        addres_ = f"{address["city"]} {address["line1"]} {address["line2"]} {address["postal_code"]}"
        phone = session["customer_details"]["phone"]
        city = address["city"]
        postal = address["postal_code"]
        country = address["country"]

        try:
            Order.objects.create(
                                user=user,
                                full_name=customer_name,
                                phone_number=phone,
                                email=customer_email,
                                delivery_address=addres_,
                                city=city,
                                postal_code=postal,
                                country=country,
                                status="Purchase was succesfull"
                            )
        except:
            print(f"Error creating order: {str(e)}")
            return HttpResponse(status=500)
    return HttpResponse(status=200)

    
class Success(TemplateView):
    template_name='orders/sucess.html'
    

    def get_context_data(self, **kwargs):
        products = self.request.session.get("carts", {})
        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user).order_by('-id').first()
        

        if order.status!="Purchase was succesfull":
            return redirect("main")
        try:
            products = self.request.session.get("carts", {})
            
            for key, item in products.items():
                
                
                 
                OrderItem.objects.create(
                                    order=order,
                                    product=Products.objects.get(name = item["product_name"]),
                                    name=item["product_name"],
                                    price=item["price"],
                                    quantity=item["quantity"],
                                    size=ProductSizeQuantity.objects.get(id = item["size_id"])
                                )
                
            del self.request.session['carts']
            self.request.session.modified = True
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            return HttpResponse(status=500)
        
        context = super().get_context_data(**kwargs)
        context['content']='Main page of website'
        
        return context
    
class Cancel(TemplateView):
    template_name='orders/fail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content']='Cancel Payment'
        return context




# class CreateOrderView(LoginRequiredMixin,FormView):
#     template_name = 'orders/create_order.html'
#     form_class = CreateOrderForm
#     succes_url = reverse_lazy("user:profile")

#     def get_initial(self):
#         initial = super().get_initial()
#         initial['full_name'] = f"{self.request.user.first_name} {self.request.user.last_name}"
#         initial['email'] = self.request.user.email
#         return initial

#     def form_valid(self, form):
#         try:
#             with transaction.atomic():
#                     user = self.request.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # Create the order
#                         order = Order.objects.create(
#                             user=user,
#                             full_name=form.cleaned_data['full_name'],
#                             phone_number=form.cleaned_data['phone_number'],
#                             email=form.cleaned_data['email'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             city=form.cleaned_data['city'],
#                             postal_code=form.cleaned_data['postal_code'],
#                             country=form.cleaned_data['country'],
#                         )
                
#                         # Create the ordered items
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             size_instance = cart_item.size  # Get the ProductSizeQuantity instance
#                             price = cart_item.product.sell_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(
#                                     f'Does not have the right amount of {name}. Only - {product.quantity}'
#                                 )

#                             if size_instance.quantity < quantity:
#                                 raise ValidationError(
#                                     f'Does not have the right amount of size {size_instance.size}. Only - {size_instance.quantity}'
#                                 )

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                                 size=size_instance,  # Pass the ProductSizeQuantity instance
#                             )
#                             product.quantity -= quantity
#                             size_instance.quantity -= quantity  # Update the size quantity
#                             product.save()
#                             size_instance.save()

                        

#                         messages.success(self.request, 'Order placed!')
#                         return redirect(reverse('order:checkout'))

#         except ValidationError as e:
#             messages.error(self.request, str(e))
#             return redirect('cart:order')
        
#     def form_invalid(self, form):
#         messages.error(self.request, 'Fill all the fields please!')
#         return redirect('orders:create_order')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Order Create'
#         return context
    

    


# def create_order(request):
#     if request.method == 'POST':
#         form = CreateOrderForm(data=request.POST)
#         print(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # Create the order
#                         order = Order.objects.create(
#                             user=user,
#                             full_name=form.cleaned_data['full_name'],
#                             phone_number=form.cleaned_data['phone_number'],
#                             email=form.cleaned_data['email'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             city=form.cleaned_data['city'],
#                             postal_code=form.cleaned_data['postal_code'],
#                             country=form.cleaned_data['country'],
#                         )
                
#                         # Create the ordered items
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.sell_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(
#                                     f'Does not have right amount of {name}. Only - {product.quantity}'
#                                 )

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save()

#                         cart_items.delete()

#                         messages.success(request, 'Order placed!')
#                         return redirect('user:profile')

#             except ValidationError as e:
#                 messages.error(request, str(e))
#                 return redirect('cart:order')
#     else:
#         print(333333333333333333)
#         # Set initial data with `full_name`
#         try:
#             initial = {
#                 'first_name': request.user.first_name,
#                 'last_name': request.user.last_name,
#                 }
#             form = CreateOrderForm(initial=initial)
#         except:
#             #messages.success("You should login first")
#             return redirect('user:login')


#     context = {"form": form, "show_checkout_button": True}
#     return render(request, 'orders/create_order.html', context)
