from django.contrib import admin
from django.urls import path, include
from carts.views import *


urlpatterns = [
    path('cart_add/<slug:product_slug>/', cart_add, name='cart_add'),
    path('cart_change/<slug:product_slug>/', cart_change, name='cart_change'),
    path('cart_remove/<slug:product_slug>/', cart_remove, name='cart_remove'),
    ]