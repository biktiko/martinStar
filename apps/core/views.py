from django.shortcuts import render
from apps.catalog.models import Category, Brand

def index(request):
    brands = Brand.objects.all()
    categories = Category.objects.filter(is_active=True)
    
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        categories = categories.filter(brands__slug__in=selected_brands).distinct()
        
    context = {
        'categories': categories,
        'brands': brands,
        'selected_brands': selected_brands,
    }
    return render(request, 'index.html', context)
