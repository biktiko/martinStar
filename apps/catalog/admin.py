from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from modeltranslation.admin import TranslationAdmin
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from .models import Category, Product, Brand, ProductOption, HeroBanner

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
    fields = ('weight', 'barcode', 'box_dimensions', 'box_dimensions_unit', 'packing_options', 'image', 'is_active')

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

@admin.register(HeroBanner)
class HeroBannerAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('id', 'placement', 'is_active', 'show_on_mobile', 'show_on_desktop', 'order')
    list_editable = ('is_active', 'show_on_mobile', 'show_on_desktop', 'order')
    list_filter = ('placement', 'is_active')
    
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE()}
    }
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.6.1/cropper.min.css',)
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.6.1/cropper.min.js',
            'js/admin_cropper.js',
        )
    
    fieldsets = (
        ('Placement & Status', {
            'fields': ('placement', 'is_active', 'show_on_mobile', 'show_on_desktop', 'order', 'banner_link')
        }),
        ('Text Overlay', {
            'fields': ('show_text_overlay', 'title', 'subtitle'),
            'description': 'Text that will be rendered on top of the banner media. You can format color, size, etc.'
        }),
        ('Desktop Media', {
            'fields': ('image', 'video_file'),
            'description': 'Banner assets for wide screens. Video will override image if both are provided.'
        }),
        ('Mobile Media', {
            'fields': ('image_mobile', 'video_file_mobile'),
            'description': 'Banner assets for vertical/mobile screens. If empty, desktop assets will be used.'
        }),
    )
