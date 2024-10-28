from django.shortcuts import render,get_object_or_404,get_list_or_404
from goods.models import Categories, Products
from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, DecimalField
from goods.utils import q_search,anotation

def catalog(request, category_slug=None):

    page = request.GET.get('page',1)#GET request from page
    on_sale=request.GET.get('discount',None)#GET request from is_onsale
    price_under_120=request.GET.get('price_under_120',None)#GET request from price_under_120
    order_by=request.GET.get('sort',None)#GET request from sort
    query=request.GET.get('q', None)#GET request from q
    
    #Showing the products by categories or by q 
    if category_slug=='all-items':
        products=Products.objects.all()
    elif query:
        products=q_search(query)
    else:
        products=Products.objects.filter(category__slug=category_slug)
        
    #Check box if the products on sale
    if on_sale: 
        products=products.filter(descount__gt=0)

    products = anotation(products)#Anotaion for low-to-high and high-to-low

    #Check box if the products price under 120
    if price_under_120:
        products=products.filter(sell_price__lt=120)
    

    # Sort by sell_price or the newest
    if order_by == 'low-to-high':
        products = products.order_by('sell_price')
    elif order_by == 'high-to-low':
        products = products.order_by('-sell_price')
    elif order_by == '-id':
        products = products.order_by('-id')
    
    
    #Pagination
    paginator=Paginator(products, 6)
    current_page=paginator.page(int(page))

    context={'title': 'Catalog',
             'products':current_page,
             'slug_url':category_slug,
             'curren_num_page':int(page),
             "show_checkout_button":True,
             }
    
    return render(request, 'goods/catalog.html',context)


def product(request, product_slug):
    product=get_object_or_404(Products, slug=product_slug)
    
    context={'title': product,
             'product':product}
    return render(request, 'goods/product.html',context)
