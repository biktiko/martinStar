from django.db import models
from django.core.cache import cache
from apps.core.image_optimization import optimize_image
from django_editorjs_fields import EditorJsJSONField

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

    featured_news_layout = models.CharField(
        max_length=10,
        blank=True,
    )

    logistics_layout = models.CharField(
        max_length=10,
        choices=[('SPLIT', 'Modern Split Grid'), ('CARD', 'Floating Card Over Banner')],
        default='SPLIT',
        help_text="Toggle the visual style of the Logistics section on the partnership page."
    )

    hr_email = models.EmailField(
        default='hr@martinstar.am',
        help_text="Main email for receiving job applications."
    )
    hr_cc_emails = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated list of CC emails (e.g., marketing@martinstar.am, ceo@martinstar.am)."
    )

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

class FooterSettings(models.Model):
    # Contacts
    phone_1 = models.CharField(max_length=50, blank=True)
    phone_2 = models.CharField(max_length=50, blank=True)
    address_text = models.TextField(blank=True, help_text="Physical address shown in footer")
    contact_email = models.EmailField(blank=True)

    # Social Media
    social_fb = models.URLField("Facebook URL", blank=True)
    social_vk = models.URLField("VKontakte URL", blank=True)
    social_instagram = models.URLField("Instagram URL", blank=True)
    social_linkedin = models.URLField("LinkedIn URL", blank=True)
    social_tiktok = models.URLField("TikTok URL", blank=True)
    social_youtube = models.URLField("YouTube URL", blank=True)

    # Martin App
    app_download_url = models.URLField(blank=True, help_text="e.g. http://ma1.am")
    app_qr_code = models.ImageField(upload_to='footer/', blank=True, null=True, help_text="QR Code for desktop footer")

    # Copyright
    copyright_text = models.CharField(max_length=255, blank=True, default="© 2026 Martin Star. All rights reserved.")

    class Meta:
        verbose_name = 'Footer Setting'
        verbose_name_plural = 'Footer Settings'

    def __str__(self):
        return "Global Footer Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete('footer_settings')

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class FooterCompanyLink(models.Model):
    settings = models.ForeignKey(FooterSettings, related_name='company_links', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255, help_text="URL or relative path like /about/")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Company Link'
        verbose_name_plural = 'Company Links'

    def __str__(self):
        return self.title

class CompanyHistory(models.Model):
    year = models.IntegerField(unique=True)
    title = models.CharField(max_length=255, help_text="Short milestone title (e.g., Canned goods production start)")
    description = models.TextField(blank=True, help_text="Optional longer description")
    image = models.ImageField(upload_to='about/history/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['year']
        verbose_name = "Company Milestone"
        verbose_name_plural = "Company Milestones"

    def __str__(self):
        return f"{self.year} - {self.title}"


class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partners/', help_text="Partner logo (transparent PNG/SVG recommended)")
    is_active = models.BooleanField(default=True)
    show_on_online_store = models.BooleanField(default=False, verbose_name="Show in Buy Online")
    show_on_partners_page = models.BooleanField(default=True, verbose_name="Show on Partners Page")
    online_store_link = models.URLField(blank=True, null=True, verbose_name="Buy Online Link")
    partner_page_link = models.URLField(blank=True, null=True, verbose_name="Partner Official Page Link")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.logo and not self.logo.name.lower().endswith(('.webp', '.svg', '.gif')):
            self.logo = optimize_image(self.logo)
        super().save(*args, **kwargs)


class ExportCountry(models.Model):
    REGION_CHOICES = [
        ('Australia', 'Australia & Oceania'),
        ('Asia', 'Asia'),
        ('North America', 'North America'),
        ('South America', 'South America'),
        ('Africa', 'Africa'),
        ('Europe', 'Europe'),
    ]
    name = models.CharField(max_length=100, help_text="Название страны (например: Россия)")
    map_code = models.CharField(max_length=5, help_text="Код страны для карты (ISO 3166-1 alpha-2, например: RU, US, AM)")
    region = models.CharField(max_length=50, choices=REGION_CHOICES, default='Europe')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Export Country'
        verbose_name_plural = 'Export Countries'
        ordering = ['region', 'name']

    def __str__(self):
        return f"{self.name} ({self.map_code})"

class BranchOffice(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Yandex Map Latitude (e.g., 40.1872)")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Yandex Map Longitude (e.g., 44.5152)")
    is_headquarters = models.BooleanField(default=False, help_text="Pin this as the main HQ at the top of the page")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_headquarters', 'order']
        verbose_name = 'Branch Office'
        verbose_name_plural = 'Branch Offices'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=100, blank=True)
    description = EditorJsJSONField(
        plugins=[
            "@editorjs/paragraph",
            "@editorjs/header",
            "@editorjs/list",
            "@editorjs/marker",
        ],
        null=True,
        blank=True,
        help_text="Full vacancy description using blocks."
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title
