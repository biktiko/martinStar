from django.shortcuts import render
from django.views.decorators.cache import cache_page
from apps.core.models import SiteSettings, CompanyHistory
from apps.catalog.models import Category, Brand, HeroBanner
from apps.blog.models import Post

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
        
    favourite_posts = Post.objects.filter(is_favourite=True, is_active=True).select_related('topic').order_by('-created_at')[:3]
        
    context = {
        'categories': categories,
        'brands': brands,
        'selected_brands': selected_brands,
        'mobile_banners': mobile_banners,
        'desktop_banners': desktop_banners,
        'favourite_posts': favourite_posts,
        'settings': SiteSettings.load(),
    }
    return render(request, 'index.html', context)

def about(request):
    history_milestones = CompanyHistory.objects.filter(is_active=True).order_by('year')
    banner = HeroBanner.objects.filter(placement='ABOUT', is_active=True).first()
    context = {
        'history_milestones': history_milestones,
        'banner': banner,
    }
    return render(request, 'about.html', context)
