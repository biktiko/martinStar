from django.shortcuts import render
from apps.catalog.models import Category

def index(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'index.html', {'categories': categories})
