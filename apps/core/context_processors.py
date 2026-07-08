from .models import SiteSettings, FooterSettings

def site_settings(request):
    return {
        'site_settings': SiteSettings.load(),
        'footer_settings': FooterSettings.load(),
    }
