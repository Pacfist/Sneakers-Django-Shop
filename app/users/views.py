from django.shortcuts import render,redirect
from users.forms import UserLoginForm
from django.contrib import auth
def login(request):
    if request.method == 'POST':

        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return redirect('users/profile.html')
    else:
        form = UserLoginForm()
    context={
        'title':'Log In',
        'form':form,
    }
    return render(request,'users/login.html', context,)


def registration(request):
    context={
        'title':'Register'
    }
    return render(request,'users/registration.html', context)


def profile(request):
    context={
        'title':'My Profile'
    }
    return render(request,'users/profile.html', context)


def logout(request):
    context={
        'title':'Log Out'
    }
    return render(request,'users/login.html', context)
