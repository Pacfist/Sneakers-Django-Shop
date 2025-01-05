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
from goods.models import Products


class UserLoginView(LoginView):

    template_name="users/login.html"
    form_class = UserLoginForm
    success_url=reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context




class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.save(commit=False)  # Save form data but do not commit yet (optional for additional customizations)
        user.save()  # Save the user to the database
        auth.login(self.request, user)  # Log in the user
        messages.success(self.request, f"{user.username}, You successfully registered")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context


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




# class UserCartView(LoginRequiredMixin,TemplateView):
#     template_name = "users/users_cart.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["show_checkout_button"] = False
#         context['title'] = 'Cart'
#         return context

# class UserCartView(TemplateView):
#     template_name = "users/users_cart.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Retrieve the cart from the session
#         cart = self.request.session.get("carts", {})

#         print(cart)
#         context["cart"] = cart
#         context['title'] = 'Cart'
#         return context
    
@login_required   
def user_cart(request):
    cart = request.session.get("carts", {})
    total_price = 0
    total_quantity = 0
    image_urls=[]
    for key,item in cart.items():
        total_price += item['price'] * item['quantity']
        total_quantity += item['quantity']
    print(f"cart is in view = {cart}")
    context = {"temp":cart, "total_quantity": total_quantity, "total_price":total_price}
    return render(request, 'users/users_cart.html', context)
    

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