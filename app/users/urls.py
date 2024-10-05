from django.contrib import admin
from django.urls import path, include
from users.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', login, name='login'),
    path('users-cart/', user_cart, name='user_cart'),
    path('registration',registration,name="registration"),
    path('profile',profile,name="profile"),
    path('logout',logout,name="logout"),
    ]

