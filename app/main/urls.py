from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
]