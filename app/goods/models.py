from django.db import models

class Categories(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, blank=True, unique=True, null=True)

    class Meta:
        db_table='category'
        ordering=("id", )

    def __str__(self):
        return self.name

class Products(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, blank=True, unique=True, null=True)
    description=models.TextField(blank=True, null=True)
    image=models.ImageField(upload_to='goods_images',blank=True, null=True )
    price=models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    descount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    quantity=models.PositiveBigIntegerField(default=0)
    category=models.ForeignKey(to=Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def display_id(self):
        return f"{self.id:05}"
    
    def sell_price(self):
        if self.descount:
            return round(self.price - self.price*self.descount/100,2)
        return self.price




