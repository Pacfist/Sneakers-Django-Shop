from django.contrib import admin
from django.urls import path, include
from main.views import IndexView, AboutView  # Import IndexView and about directly
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Use IndexView here
    path('about/', cache_page(60) (AboutView.as_view()), name='about'),
]
