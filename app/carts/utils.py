# from carts.models import Cart

# def get_user_carts(request):
#     if request.user.is_authenticated:
#         return Cart.objects.filter(user=request.user).select_related('product')
    
    
#     if not request.session.session_key:
#         request.session.create()
        
#     return Cart.objects.filter(session_key=request.session.session_key).select_related('product')


def get_user_carts(request):
    # Retrieve the cart from the session
    cart = request.session.get("cart", {})

    # Transform the session cart data into a more readable format
    user_cart = []
    for item_key, item_data in cart.items():
        user_cart.append({
            "product_id": item_data["product_id"],
            "size_id": item_data["size_id"],
            "quantity": item_data["quantity"],
            "product_name": item_data.get("product_name"),  # Include optional product details
            "size_name": item_data.get("size_name"),        # Include optional size details
        })
    
    return user_cart