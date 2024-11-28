from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from users.forms import ProfileUser,UserLoginForm,UserRegistrationForm
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from carts.models import Cart
from orders.models import Order ,OrderItem
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.cache import cache
from common.mixins import CacheMixin
# def login(request):#login for user
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)#using login form from forms.py
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             session_key=request.session.session_key
#             user = auth.authenticate(username=username,password=password)#authenticate user
#             if user:
#                 auth.login(request,user)
#                 messages.success(request, f"{username}, entered in the account")
#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#                 return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = UserLoginForm()
#     context={
#         'title':'Log In',
#         'form':form,
#     }
#     return render(request,'users/login.html', context,)

class UserLoginView(LoginView):

    template_name="users/login.html"
    form_class = UserLoginForm
    success_url=reverse_lazy('main:index')

    # def get_success_url(self):
    #     return reverse_lazy('main:index')
    
    # def form_valid(self, form):
    #     session_key = self.request.session.session_key

    #     user = form.get_user()

    #     if user:
    #         auth.login(self.request, user)
    #         if session_key:
    #             # delete old authorized user carts
    #             forgot_carts = Cart.objects.filter(user=user)
    #             if forgot_carts.exists():
    #                 forgot_carts.delete()
    #             # add new authorized user carts from anonimous session
    #             Cart.objects.filter(session_key=session_key).update(user=user)

    #             messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")

    #             return reverse_lazy('main:index')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['title'] = 'Login'
        return context


# def registration(request):#registration for user

#     if request.method == 'POST':

#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             user=form.instance
#             session_key=request.session.session_key
#             auth.login(request, user)
#             if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#             messages.success(request, f"{user.username}, created in the account")
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = UserRegistrationForm()

#     context={
#         'title':'Register',
#         'form': form,
#     }
#     return render(request,'users/registration.html', context)

class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        session_key=self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        messages.success(self.request, f"{user.username}, You successfuly registered")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context



# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileUser(data=request.POST, files=request.FILES, instance=request.user)
#         if form.is_valid():
#             print(request.FILES)
#             form.save()
#             messages.success(request, "Profiled was updated!")
#             return redirect(reverse('user:profile'))
        
#     else:
#         form = ProfileUser(instance=request.user)
        
#     orders=(Order.objects.filter(user=request.user).prefetch_related(
#         Prefetch("orderitem_set",
#                  queryset=OrderItem.objects.select_related("product"),
#         )
#     )
#     .order_by("-id")
#     )
#     print(orders)
#     context = {
#         'form': form,
#         'user': request.user,
#         'orders':orders,
#     }
#     return render(request, 'users/profile.html', context)


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileUser
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset = None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile was updated!')
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Profile'

        
        
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product").order_by("-id"),
            )
        )
            
        context['orders'] = self.set_get_cashe(orders, f"user_{self.request.user.id}_orders", 60*2)

        return context
    




@login_required
def logout(request):
    messages.success(request, "You logged out!")
    auth.logout(request)
    return redirect(reverse('index'))


# @login_required   
# def user_cart(request):
#     return render(request, 'users/users_cart.html', {"show_checkout_button":False})


class UserCartView(LoginRequiredMixin,TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_checkout_button"] = False
        context['title'] = 'Cart'
        return context
    
