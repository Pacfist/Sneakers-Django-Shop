from django.db import models
from users.models import User
from goods.models import Products,ProductSizeQuantity

class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        else:
            return 0
        
class Cart(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE,blank=True, null=True)
    product= models.ForeignKey(to=Products,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField(default=0)
    size = models.ForeignKey(to=ProductSizeQuantity, on_delete=models.CASCADE, null=True, blank=True)
    created_timestamp=models.DateTimeField(auto_now_add=True)
    session_key=models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table='cart'

    objects=CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.sell_price()*self.quantity,2)

    def __str__(self):
        if self.user:
            return f"Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}"
        else:
            return f"Cart (Session: {self.session_key}) | Product {self.product.name} | Quantity {self.quantity}"
        

class Comments(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.body[0:50]