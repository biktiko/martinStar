"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from apps.core.views import index

urlpatterns = [
    # Non-translatable URLs can go here
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    prefix_default_language=False, # Don't add /hy/ for the default language
)
