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
