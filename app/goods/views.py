from django.shortcuts import render,get_object_or_404
from goods.models import Categories, Products
from django.core.paginator import Paginator
from goods.utils import q_search,anotation
from django.http import Http404
from django.views.generic import DetailView, ListView 

# def catalog(request, category_slug=None):

#     page=request.GET.get('page',1)#GET request from page
#     on_sale=request.GET.get('discount',None)#GET request from is_onsale
#     price_under_120=request.GET.get('price_under_120',None)#GET request from price_under_120
#     order_by=request.GET.get('sort',None)#GET request from sort
#     query=request.GET.get('q', None)#GET request from q
    
#     #Showing the products by categories or by q 
#     if category_slug=='all-items':
#         products=Products.objects.all()
#     elif query:
#         products=q_search(query)
#     else:
#         products=Products.objects.filter(category__slug=category_slug)
        
#     #Check box if the products on sale
#     if on_sale: 
#         products=products.filter(descount__gt=0)

#     products = anotation(products)#Anotaion for low-to-high and high-to-low

#     #Check box if the products price under 120
#     if price_under_120:
#         products=products.filter(sell_price__lt=120)
    
#     # Sort by sell_price or the newest
#     if order_by == 'low-to-high':
#         products = products.order_by('sell_price')
#     elif order_by == 'high-to-low':
#         products = products.order_by('-sell_price')
#     elif order_by == '-id':
#         products = products.order_by('-id')
    
#     #Pagination
#     paginator=Paginator(products, 6)
#     current_page=paginator.page(int(page))

#     context={'title': 'Catalog',
#              'products':current_page,
#              'slug_url':category_slug,
#              'curren_num_page':int(page),
#              }
    
#     return render(request, 'goods/catalog.html',context)

class CatalogView(ListView):
    model = Products
    template_name="goods/catalog.html"
    context_object_name = "products" 
    paginate_by = 6

    def get_queryset(self):
         
        category_slug = self.kwargs.get("category_slug")
        query = self.kwargs.get("q")
        on_sale = self.kwargs.get("on_sale")
        order_by = self.kwargs.get("order_by")
        price_under_120 = self.kwargs.get("price_under_120")
        
        #Showing the products by categories or by q 
        if category_slug=='all-items':
            products=super().get_queryset() #Same as Products.objects.all()
        elif query:
            products=q_search(query)
        else:
            products=super().get_queryset().filter(category__slug=category_slug)
            
            
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

        return products
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Catalog"
        context['slug_url'] = self.kwargs.get("category_slug")
        return context
    
     


# def product(request, product_slug):
#     product=get_object_or_404(Products, slug=product_slug)
#   
#     context={'title': product,
#              'product':product}
#     return render(request, 'goods/product.html',context)


class ProductView(DetailView):
    #model = Products
    #slug_field = 'slug'
    template_name="goods/product.html"
    slug_url_kwarg="product_slug"
    context_object_name = 'product'

    def get_object(self):
        product = get_object_or_404(Products, slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        print(self.object.price)
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
    
