from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand

def category_products_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    products = Product.objects.filter(category=category, is_active=True).prefetch_related('options')
    
    # Get all brands that have products in this category
    brand_ids = products.values_list('brand_id', flat=True).distinct()
    brands = Brand.objects.filter(id__in=brand_ids)
    
    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand__slug=selected_brand)
        
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail_view(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    product = get_object_or_404(Product.objects.prefetch_related('options'), slug=product_slug, category=category, is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'category': category,
        'product': product,
        'categories': categories,
    }
    return render(request, 'catalog/product_detail.html', context)
