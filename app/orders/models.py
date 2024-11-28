from django.db import models
from users.models import User
from goods.models import Products,ProductSizeQuantity


class OrderitemQueryset(models.QuerySet):
     def total_price(self):
        return sum(cart.products_price() for cart in self)
    
     def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()  # To store email from the form
    full_name = models.CharField(max_length=100)  # Full name field from the form
    delivery_address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    postal_code = models.CharField(max_length=20,null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)
    
    
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='Processing...')
    
    # Payment information fields
    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(max_length=4)
    

    def __str__(self):
        return f"Order {self.pk} | Buyer {self.user.first_name}"
    class Meta:
        ordering = ['-id'] 

    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, default=None)
    size = models.ForeignKey(to=ProductSizeQuantity, on_delete=models.SET_DEFAULT, null=True,blank = True, default=None)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderitemQueryset.as_manager()

    def product_price(self):
        return round(self.price()*self.quantity,2)
    
    def __str__(self):
        return f"Item {self.name} | Order {self.order.pk}"