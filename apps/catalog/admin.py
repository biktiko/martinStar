from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product, Brand, ProductOption

@admin.register(Category)
class CategoryAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    # Can also define fieldsets or just fields
    fields = ('name', 'slug', 'description', 'icon', 'image', 'is_active', 'brands', 'meta_title', 'meta_description')
    filter_horizontal = ('brands',)

class ProductOptionInline(TabularInline):
    model = ProductOption
    extra = 1
    fields = ('weight', 'barcode', 'box_dimensions', 'box_dimensions_unit', 'packing_options', 'packing_options_unit', 'image', 'is_active')

@admin.register(Product)
class ProductAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('name', 'category', 'brand', 'is_active')
    list_filter = ('is_active', 'category', 'brand')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductOptionInline]
    
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'slug', 'category', 'brand', 'is_active', 'description', 'image')
        }),
        ('Storage Requirements', {
            'fields': ('min_storage_temp', 'max_storage_temp', 'storage_period_days')
        }),
        ('Nutrition Information', {
            'fields': ('calories', 'proteins', 'fats', 'carbohydrates')
        }),
        ('SEO Optimization', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
    )

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
