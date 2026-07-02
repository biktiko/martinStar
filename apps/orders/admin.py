from django.contrib import admin
from .models import Cart, Order, DeliveryAddress, Courier

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_address')

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'is_active')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at')
