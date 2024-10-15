from django.contrib import admin
from django.urls import path, include
from carts.views import *


urlpatterns = [
    path('cart_add/', cart_add, name='cart_add'),
    path('cart_change/', cart_change, name='cart_change'),
    path('cart_remove/<int:cart_id>/', cart_remove, name='cart_remove'),
    ]