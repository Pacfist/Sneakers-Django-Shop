from django.shortcuts import render
from goods.models import Categories, Products

def catalog(request):
    categories=Categories.objects.all()
    products=Products.objects.all()
    context={'title': 'Catalog',
             'categories':categories,
             'products':products,
             'i':[1,2,3,4,5,6,7,8,9,10,11]}
    return render(request, 'goods/catalog.html',context)


def product(request):
    context={'title': 'Product'}
    return render(request, 'goods/product.html',context)
