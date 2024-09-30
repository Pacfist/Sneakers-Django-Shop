from django.shortcuts import render,get_object_or_404,get_list_or_404
from goods.models import Categories, Products
from django.core.paginator import Paginator

def catalog(request, category_slug):

    page = request.GET.get('page',1)

    if category_slug=='all-items':
        products=Products.objects.all()
    else:
        products=get_list_or_404(Products,category__slug=category_slug)

    paginator=Paginator(products, 3)
    current_page=paginator.page(int(page))

    context={'title': 'Catalog',
             'products':current_page,
             'slug_url':category_slug,
             'curren_num_page':int(page),
             }
    return render(request, 'goods/catalog.html',context)


def product(request, product_slug):
    product=get_list_or_404(Products, slug=product_slug)
    print(product.price)
    print('---------------------------------------------------')
    context={'title': product,
             'product':product}
    return render(request, 'goods/product.html',context)
