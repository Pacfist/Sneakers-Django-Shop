from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Products


class IndexView(TemplateView):
    template_name='main/main.html'

    def get_context_data(self, **kwargs):
        cart = self.request.session.get("carts", {})
        context = super().get_context_data(**kwargs)
        products = Products.objects.order_by('-id')[:3]
        context['title']='Home'
        context['content']='Main page of website'
        context['products'] = products
        context['temp'] = cart
        return context


def index(request):
      context={
          'title':'Home page',
         'content':'Main page of website',
        
          }
      return render(request, 'main/main.html',context)

# def about(request):
#     context={
#         'title':'About',
#         'content':'Main page of website'
#     }
#     return render(request, 'main/about.html',context)



class AboutView(TemplateView):
    template_name='main/about.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['title']='About'
        context['content_info']='About the sneaker shop'
        return context