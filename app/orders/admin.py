from django.contrib import admin
from carts.admin import  CartTabAdmin
from orders.models import Order, OrderItem

class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        'id', 'city', 
        'country', 'postal_code', 'created_timestamp', 'is_paid', 'status'
    )

    readonly_fields = ("created_timestamp",)
    extra = 0


#class OrderItemTabilareAdmin(admin.TabularInline):
    #model = OrderItem
    #fields = "product", "name", "price", "quantity"
    #extra = 0



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
    list_display = ['order', 'product', 'name', 'price', 'quantity',]
    search_fields = ['name', 'order__id']
    ordering = ['-created_timestamp']
