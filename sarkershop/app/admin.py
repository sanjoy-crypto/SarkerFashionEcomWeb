from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(OrderPlaced)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone',
                    'locality', 'city', 'division')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'Selling_price', 'discount_price',
                    'description', 'brand', 'category', 'product_image')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'product',
                    'quantity', 'ordered_date', 'status')
