from django.contrib import admin
from carts.admin import  CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    search_fields=['username','first_name', 'last_name', 'email']
    list_display=['username','first_name', 'last_name', 'email']


    inlines=[CartTabAdmin,OrderTabulareAdmin ]