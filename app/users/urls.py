from django.urls import path
from users.views import login, user_cart, registration, profile, logout

app_name = 'user'  # Define the namespace here

urlpatterns = [
    path('login', login, name='login'),
    path('users-cart/', user_cart, name='user_cart'),
    path('registration', registration, name="registration"),
    path('profile', profile, name="profile"),
    path('logout', logout, name="logout"),
]
