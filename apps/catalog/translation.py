from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, HeroBanner

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'meta_title', 'meta_description')

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'name', 'description', 
        'meta_title', 'meta_description'
    )

@register(HeroBanner)
class HeroBannerTranslationOptions(TranslationOptions):
    fields = ('image',)
