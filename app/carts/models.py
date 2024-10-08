from django.db import models
from users.models import User
from goods.models import Products

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
    created_timestamp=models.DateTimeField(auto_now_add=True)
    session_key=models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table='cart'

    objects=CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.sell_price()*self.quantity,2)

    def __str__(self):
        return f"Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}"