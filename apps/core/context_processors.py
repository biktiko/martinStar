from django.conf import settings
from .models import SiteSettings, FooterSettings

def site_settings(request):
    return {
        'site_settings': SiteSettings.load(),
        'footer_settings': FooterSettings.load(),
        'amplitude_api_key': getattr(settings, 'AMPLITUDE_API_KEY', ''),
    }
