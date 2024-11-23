from django.contrib import admin
from django.urls import path, include
from main.views import IndexView, AboutView  # Import IndexView and about directly

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Use IndexView here
    path('about/', AboutView.as_view(), name='about'),
]
