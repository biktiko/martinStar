from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings, FooterCompanyLink, FooterSettings, CompanyHistory

@register(FooterSettings)
class FooterSettingsTranslationOptions(TranslationOptions):
    fields = ('address_text', 'copyright_text')

@register(FooterCompanyLink)
class FooterCompanyLinkTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(CompanyHistory)
class CompanyHistoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

