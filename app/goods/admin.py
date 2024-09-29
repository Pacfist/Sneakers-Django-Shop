from django.contrib import admin
from goods.models import Categories, Products

@admin.register(Categories)
class CaregoriesAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}