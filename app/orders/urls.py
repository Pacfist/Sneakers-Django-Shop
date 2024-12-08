from django.urls import path,re_path

from orders import views 

app_name='orders'

urlpatterns=[
    #path('create-order/', views.CreateOrderView.as_view(), name='create_order',),
    path('checkout-session/', views.CreateCheckout.as_view(), name='checkout'),
    path('success/', views.Success.as_view(), name='success'),
    path('cancel/', views.Cancel.as_view(), name='cancel'),
    re_path(r'^webhook/?$', views.my_webhook_view, name='webhook'),  # Matches both /webhook and /webhook/
    ]