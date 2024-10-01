from django.shortcuts import render,get_object_or_404,get_list_or_404
from goods.models import Categories, Products
from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, DecimalField

def catalog(request, category_slug):

    page = request.GET.get('page',1)
    on_sale=request.GET.get('discount',None)
    price_under_120=request.GET.get('price_under_120',None)
    order_by=request.GET.get('sort',None)
    

    if category_slug=='all-items':
        products=Products.objects.all()
    else:
        products=Products.objects.filter(category__slug=category_slug)
        
    print(on_sale)
    if on_sale:
        products=products.filter(descount__gt=0)

    

    products = products.annotate(
        sell_price=ExpressionWrapper(
            F('price') - F('price') * F('descount') / 100,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    if price_under_120:
        products=products.filter(sell_price__lt=120)
    

    # Sort by sell_price
    if order_by == 'low-to-high':
        products = products.order_by('sell_price')
    elif order_by == 'high-to-low':
        products = products.order_by('-sell_price')
    elif order_by == '-id':
        products = products.order_by('-id')
    
    
    
    paginator=Paginator(products, 6)
    current_page=paginator.page(int(page))

    context={'title': 'Catalog',
             'products':current_page,
             'slug_url':category_slug,
             'curren_num_page':int(page),
             }
    return render(request, 'goods/catalog.html',context)


def product(request, product_slug):
    product=get_object_or_404(Products, slug=product_slug)
    
    context={'title': product,
             'product':product}
    return render(request, 'goods/product.html',context)
