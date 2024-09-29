from django.shortcuts import render
from goods.models import Categories, Products

def catalog(request):
    products=Products.objects.all()

    context={'title': 'Catalog',
             'products':products,
             }
    return render(request, 'goods/catalog.html',context)


def product(request):
    
    context={'title': 'Product',}
    return render(request, 'goods/product.html',context)
