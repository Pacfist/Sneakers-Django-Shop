from django.contrib import admin

from carts.models import Cart,Comments

class CartTabAdmin(admin.TabularInline):
    model = Cart 
    fields = "product", "quantity", "created_timestamp"
    search_fields="product", "quantity", "created_timestamp"
    readonly_fields=("created_timestamp",)
    extra=1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user_display', 'product', 'quantity', 'created_timestamp']
    list_filter=['created_timestamp', 'user', 'product__name']
    
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Anonymus"
    
    def product_display(self, obj):
        return str(obj.product.name)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display=['user', 'product', 'body', 'updated', 'created']