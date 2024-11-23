from django.contrib import admin
from django.urls import path, include
from goods.views import *

urlpatterns = [
    path('search/', CatalogView.as_view(), name = 'search'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name='product'),
] 