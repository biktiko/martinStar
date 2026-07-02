from django.db import models
from django.conf import settings

class DeliveryAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # Placeholder for future expansion

class Courier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courier_profile')
    vehicle_type = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    # Placeholder for future expansion

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Placeholder for future expansion (CartItem models etc)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=50, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Placeholder for future expansion (OrderItems, Payment data)
