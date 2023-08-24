from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','price']
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user'] 


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','cart','product','quantity']
    


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin): 
    list_display = ['id','product_name','quantity','price']
    
