from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('login', login, name='login'),
    path('registration',registration,name="registration"),
    path('profile',profile,name="profile"),
    path('logout',logout,name="logout"),

    
]