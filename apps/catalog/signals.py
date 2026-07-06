from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Product, Brand, HeroBanner

def clear_cache_on_change(sender, **kwargs):
    """
    Clears the entire cache when any catalog-related model is modified.
    This ensures @cache_page views are immediately refreshed.
    """
    cache.clear()

# Connect the signals
for model in [Category, Product, Brand, HeroBanner]:
    post_save.connect(clear_cache_on_change, sender=model)
    post_delete.connect(clear_cache_on_change, sender=model)
