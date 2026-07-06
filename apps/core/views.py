from django.shortcuts import render
from django.views.decorators.cache import cache_page
from apps.core.models import SiteSettings
from apps.catalog.models import Category, Brand, HeroBanner

@cache_page(60 * 15)
def index(request):
    brands = Brand.objects.all()
    categories = Category.objects.filter(is_active=True)
    
    active_banners = HeroBanner.objects.filter(is_active=True)
    mobile_banners = [b for b in active_banners if b.show_on_mobile]
    desktop_banners = [b for b in active_banners if b.show_on_desktop]
    
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        categories = categories.filter(brands__slug__in=selected_brands).distinct()
        
    context = {
        'categories': categories,
        'brands': brands,
        'selected_brands': selected_brands,
        'mobile_banners': mobile_banners,
        'desktop_banners': desktop_banners,
        'settings': SiteSettings.load(),
    }
    return render(request, 'index.html', context)
