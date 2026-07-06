from django.db import models
from django.core.cache import cache

class SiteSettings(models.Model):
    class MobileGridOptions(models.TextChoices):
        GRID_2X2 = '2x2', '2x2 Grid (4 items)'
        GRID_1X2 = '1x2', '1x2 Grid (2 items side-by-side)'

    mobile_grid_layout = models.CharField(
        max_length=10,
        choices=MobileGridOptions.choices,
        default=MobileGridOptions.GRID_2X2,
        help_text="Choose the mobile category slider layout."
    )

    # Footer: Contacts
    phone_1 = models.CharField(max_length=50, blank=True)
    phone_2 = models.CharField(max_length=50, blank=True)
    address_text = models.TextField(blank=True, help_text="Physical address shown in footer")
    contact_email = models.EmailField(blank=True)

    # Footer: Social Media
    social_fb = models.URLField("Facebook URL", blank=True)
    social_vk = models.URLField("VKontakte URL", blank=True)
    social_instagram = models.URLField("Instagram URL", blank=True)
    social_linkedin = models.URLField("LinkedIn URL", blank=True)
    social_tiktok = models.URLField("TikTok URL", blank=True)
    social_youtube = models.URLField("YouTube URL", blank=True)

    # Footer: Martin App
    app_download_url = models.URLField(blank=True, help_text="e.g. http://ma1.am")
    app_qr_code = models.ImageField(upload_to='footer/', blank=True, null=True, help_text="QR Code for desktop footer")

    # Footer: Copyright
    copyright_text = models.CharField(max_length=255, blank=True, default="© 2026 Martin Star. All rights reserved.")

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Global Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete('site_settings')


    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class FooterCompanyLink(models.Model):
    settings = models.ForeignKey(SiteSettings, related_name='company_links', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255, help_text="URL or relative path like /about/")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Company Link'
        verbose_name_plural = 'Company Links'

    def __str__(self):
        return self.title


