from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import SiteSettings, FooterCompanyLink

class FooterCompanyLinkInline(TranslationTabularInline, TabularInline):
    model = FooterCompanyLink
    extra = 0
    fields = ('title', 'url', 'order')


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin, TranslationAdmin):
    inlines = [FooterCompanyLinkInline]
    
    fieldsets = (
        ('General', {
            'fields': ('mobile_grid_layout',)
        }),
        ('Footer: Contacts', {
            'fields': ('phone_1', 'phone_2', 'address_text', 'contact_email')
        }),
        ('Footer: Social Media', {
            'fields': ('social_fb', 'social_vk', 'social_instagram', 'social_linkedin', 'social_tiktok', 'social_youtube')
        }),
        ('Footer: Martin App', {
            'fields': ('app_download_url', 'app_qr_code')
        }),
        ('Footer: Copyright', {
            'fields': ('copyright_text',)
        }),
    )

    # Only allow one instance
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
