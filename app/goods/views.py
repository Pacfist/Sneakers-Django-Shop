from django.shortcuts import render,get_object_or_404
from goods.models import Categories, Products

def catalog(request):
    products=Products.objects.all()

    context={'title': 'Catalog',
             'products':products,
             }
    return render(request, 'goods/catalog.html',context)


def product(request, product_slug):
    product=get_object_or_404(Products, slug=product_slug)
    print(product.price)
    print('---------------------------------------------------')
    context={'title': product,
             'product':product}
    return render(request, 'goods/product.html',context)
