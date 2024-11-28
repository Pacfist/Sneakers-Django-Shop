from django.contrib import admin
from django.urls import path, include
from carts.views import *


urlpatterns = [
    path('cart_add/', CartAddView.as_view(), name='cart_add'),
    path('cart_remove/', CartRemoveView.as_view(), name='cart_remove'),
    path('comment/', CommentView.as_view(), name='comment'),
    ]