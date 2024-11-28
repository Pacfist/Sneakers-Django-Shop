from django.shortcuts import render, redirect
from orders.forms import CreateOrderForm
from django.db import transaction
from carts.models import Cart
from orders.models import Order, OrderItem
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy


class CreateOrderView(LoginRequiredMixin,FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    succes_url = reverse_lazy("user:profile")

    def get_initial(self):
        initial = super().get_initial()
        initial['full_name'] = f"{self.request.user.first_name} {self.request.user.last_name}"
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                    user = self.request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Create the order
                        order = Order.objects.create(
                            user=user,
                            full_name=form.cleaned_data['full_name'],
                            phone_number=form.cleaned_data['phone_number'],
                            email=form.cleaned_data['email'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            city=form.cleaned_data['city'],
                            postal_code=form.cleaned_data['postal_code'],
                            country=form.cleaned_data['country'],
                        )
                
                        # Create the ordered items
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            size_instance = cart_item.size  # Get the ProductSizeQuantity instance
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f'Does not have the right amount of {name}. Only - {product.quantity}'
                                )

                            if size_instance.quantity < quantity:
                                raise ValidationError(
                                    f'Does not have the right amount of size {size_instance.size}. Only - {size_instance.quantity}'
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                                size=size_instance,  # Pass the ProductSizeQuantity instance
                            )
                            product.quantity -= quantity
                            size_instance.quantity -= quantity  # Update the size quantity
                            product.save()
                            size_instance.save()

                        cart_items.delete()

                        messages.success(self.request, 'Order placed!')
                        return redirect('user:profile')

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('cart:order')
        
    def form_invalid(self, form):
        messages.error(self.request, 'Fill all the fields please!')
        return redirect('orders:create_order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Order Create'
        return context
    
    


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
