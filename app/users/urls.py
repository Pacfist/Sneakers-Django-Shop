from django.urls import path
from users.views import UserCartView, UserProfileView, logout, UserLoginView, UserRegistrationView

app_name = 'user'  # Define the namespace here

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('users-cart/', UserCartView.as_view(), name='user_cart'),
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('logout/', logout, name="logout"),
]
