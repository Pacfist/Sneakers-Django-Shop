from django.contrib import admin
from django.urls import path, include
from goods.views import *

urlpatterns = [
    path('<slug:category_slug>/', catalog, name='catalog'),
    path('product/<slug:product_slug>/', product, name='product'),
] 