from django.contrib import admin
from carts.admin import  CartTabAdmin
from orders.models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'full_name', 'email', 'phone_number', 'city', 
        'country', 'postal_code', 'created_timestamp', 'is_paid', 'status'
    ]
    list_filter = ['is_paid', 'status', 'country', 'created_timestamp']
    search_fields = ['user__username', 'full_name', 'email', 'phone_number']
    ordering = ['-created_timestamp']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'name', 'price', 'quantity', 'created_timestamp']
    search_fields = ['name', 'order__id']
    ordering = ['-created_timestamp']
