from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'is_active', 'updated_at')
    list_filter = ('is_active', 'category')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku', 'description')
