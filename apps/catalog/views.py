from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Category, Product, Brand, HeroBanner
from apps.core.models import SiteSettings, Partner

# @cache_page(60 * 15)
def products_view(request):
    brands = Brand.objects.all()
    categories = Category.objects.filter(is_active=True)
    
    selected_brand = request.GET.get('brand')
    if selected_brand:
        categories = categories.filter(brands__slug=selected_brand).distinct()
        
    banner = HeroBanner.objects.filter(placement='PRODUCTS', is_active=True).first()
    online_partners = Partner.objects.filter(is_active=True, show_on_online_store=True)
        
    context = {
        'categories': categories,
        'brands': brands,
        'selected_brand': selected_brand,
        'banner': banner,
        'online_partners': online_partners,
    }
    return render(request, 'catalog/products_list.html', context)

@cache_page(60 * 15)
def category_products_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    products = Product.objects.filter(category=category, is_active=True).prefetch_related('options')
    
    # Show all brands, or we could filter by ones that have products. User requested to see all 2 brands.
    brands = Brand.objects.all()
    
    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand__slug=selected_brand)
        categories = categories.filter(brands__slug=selected_brand).distinct()
        
    online_partners = Partner.objects.filter(is_active=True, show_on_online_store=True)
        
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'online_partners': online_partners,
    }
    return render(request, 'catalog/product_list.html', context)

@cache_page(60 * 15)
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

def search_products_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(options__barcode__icontains=query),
            is_active=True
        ).prefetch_related('options').distinct()
        
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'catalog/search_results.html', context)
