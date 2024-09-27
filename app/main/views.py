from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context={
        'title':'Home',
        'content':'Main page of website'
    }
    return render(request, 'main.html',context)

def about(request):
    return HttpResponse('about')
