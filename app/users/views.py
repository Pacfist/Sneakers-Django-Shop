from django.shortcuts import render,redirect,reverse
from users.forms import ProfileUser,UserLoginForm,UserRegistrationForm
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from carts.models import Cart

def login(request):#login for user
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)#using login form from forms.py
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)#authenticate user
            if user:
                auth.login(request,user)
                messages.success(request, f"{username}, entered in the account")
                return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserLoginForm()
    context={
        'title':'Log In',
        'form':form,
    }
    return render(request,'users/login.html', context,)


def registration(request):#registration for user

    if request.method == 'POST':

        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user=form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, created in the account")
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserRegistrationForm()

    context={
        'title':'Register',
        'form': form,
    }
    return render(request,'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUser(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            print(request.FILES)
            form.save()
            messages.success(request, "Profiled was updated!")
            return redirect(reverse('profile'))
        
    else:
        form = ProfileUser(instance=request.user)
        

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    messages.success(request, "You logged out!")
    auth.logout(request)
    return redirect(reverse('index'))


@login_required   
def user_cart(request):
     

    return render(request, 'users/users_cart.html')