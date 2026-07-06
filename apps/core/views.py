from django.shortcuts import render
from apps.core.models import SiteSettings
from apps.catalog.models import Category, Brand, HeroBanner

def index(request):
    brands = Brand.objects.all()
    categories = Category.objects.filter(is_active=True)
    
    banner = HeroBanner.objects.filter(is_active=True).first()
    
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        categories = categories.filter(brands__slug__in=selected_brands).distinct()
        
    context = {
        'categories': categories,
        'brands': brands,
        'selected_brands': selected_brands,
        'banner': banner,
        'settings': SiteSettings.load(),
    }
    return render(request, 'index.html', context)
