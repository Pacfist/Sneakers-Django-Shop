from django.shortcuts import render, redirect
from orders.forms import CreateOrderForm
from django.db import transaction
from carts.models import Cart
from orders.models import Order, OrderItem
from django.forms import ValidationError
from django.contrib import messages

def create_order(request):
    print(1111111111)
    if request.method == 'POST':
        print(2222222222)
        form = CreateOrderForm(data=request.POST)
        print(55555555)
        if form.is_valid():
            print(55555555)
            try:
                with transaction.atomic():
                    user = request.user
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
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f'Does not have right amount of {name}. Only - {product.quantity}'
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        cart_items.delete()

                        messages.success(request, 'Order placed!')
                        return redirect('user:profile')

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('cart:order')
    else:
        print(333333333333333333)
        # Set initial data with `full_name`
        initial = {
             'first_name': request.user.first_name,
             'last_name': request.user.last_name,
             }
        form = CreateOrderForm(initial=initial)

    context = {"form": form, "show_checkout_button": False}
    return render(request, 'orders/create_order.html', context)
