from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories
from carts.models import Cart
def index(request):

    categories=Categories.objects.all()
    
    context={
        'title':'Home page',
        'content':'Main page of website',
        
        }
    return render(request, 'main/main.html',context)

def about(request):
    context={
        'title':'About',
        'content':'Main page of website'
    }
    return render(request, 'main/about.html',context)
