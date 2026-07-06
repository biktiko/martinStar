from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings, FooterCompanyLink

@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('address_text', 'copyright_text')

@register(FooterCompanyLink)
class FooterCompanyLinkTranslationOptions(TranslationOptions):
    fields = ('title',)

