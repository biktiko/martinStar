from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import SiteSettings, FooterCompanyLink, FooterSettings, CompanyHistory, PartnerLogo, ExportCountry, BranchOffice, Vacancy

class FooterCompanyLinkInline(TranslationTabularInline, TabularInline):
    model = FooterCompanyLink
    extra = 0
    fields = ('title', 'url', 'order')


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('mobile_grid_layout', 'featured_news_layout', 'logistics_layout')
        }),
        ('HR & Careers', {
            'fields': ('hr_email', 'hr_cc_emails')
        }),
    )

    # Only allow one instance
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FooterSettings)
class FooterSettingsAdmin(ModelAdmin, TranslationAdmin):
    inlines = [FooterCompanyLinkInline]
    
    fieldsets = (
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
        return not FooterSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('year', 'title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('year', 'title', 'description')
    ordering = ('year',)

@admin.register(PartnerLogo)
class PartnerLogoAdmin(ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(ExportCountry)
class ExportCountryAdmin(ModelAdmin):
    list_display = ('name', 'map_code', 'region', 'is_active')
    list_editable = ('is_active', 'region', 'map_code')
    search_fields = ('name', 'map_code')
    list_filter = ('region', 'is_active')

@admin.register(BranchOffice)
class BranchOfficeAdmin(ModelAdmin):
    list_display = ('name', 'address', 'phone', 'is_headquarters', 'order')
    list_editable = ('is_headquarters', 'order')
    search_fields = ('name', 'address', 'phone', 'email')
    list_filter = ('is_headquarters',)

@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = ('title', 'department', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'department', 'description')
    list_filter = ('department', 'is_active')
