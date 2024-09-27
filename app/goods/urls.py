from django.contrib import admin
from django.urls import path, include
from goods.views import *

urlpatterns = [
    path('', catalog, name='catalog'),
    path('product/', product, name='product'),
] 