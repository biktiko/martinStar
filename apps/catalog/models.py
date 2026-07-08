from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.core.image_optimization import optimize_image
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    brands = models.ManyToManyField('Brand', related_name='categories', blank=True)
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            if not self.image.name.lower().endswith('.webp'):
                self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.logo:
            if not self.logo.name.lower().endswith('.webp'):
                self.logo = optimize_image(self.logo)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    
    # Unit Choices moved to ProductOption level conceptually, but can keep on Product or Option.
    # Better to keep choices globally available if needed, but they are used in ProductOption.

    min_storage_temp = models.IntegerField(null=True, blank=True, help_text="in Celsius")
    max_storage_temp = models.IntegerField(null=True, blank=True, help_text="in Celsius")
    storage_period_days = models.IntegerField(null=True, blank=True, help_text="Storage period in days")
    
    calories = models.CharField(max_length=100, blank=True, help_text="e.g., 579/2424 kcal/kJ")
    proteins = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="in grams")
    fats = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="in grams")
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="in grams")
    
    is_active = models.BooleanField(default=True)
    
    image = models.ImageField(upload_to='products/', help_text="Main cover photo for the product.")
    
    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            if not self.image.name.lower().endswith('.webp'):
                self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

class ProductOption(models.Model):
    product = models.ForeignKey(Product, related_name='options', on_delete=models.CASCADE)
    
    # Unit Choices
    class BoxDimensionUnit(models.TextChoices):
        MM = 'mm', _('mm')
        CM = 'cm', _('cm')

    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in grams")
    barcode = models.CharField(max_length=50, unique=True, null=True, blank=True)
    box_dimensions = models.CharField(max_length=100, blank=True, help_text="L x W x H (e.g., 285x315x235)")
    box_dimensions_unit = models.CharField(max_length=10, choices=BoxDimensionUnit.choices, default=BoxDimensionUnit.MM)
    packing_options = models.CharField(max_length=100, blank=True, help_text="Enter quantity in box (e.g., 50). System will auto-prepend weight (e.g., 100g/50pcs).")
    
    image = models.ImageField(upload_to='products/options/', null=True, blank=True, help_text="Specific photo for this variant. Leave blank to use main product photo.")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product Option'
        verbose_name_plural = 'Product Options'
        ordering = ['weight']

    def __str__(self):
        return f"{self.product.name} - {self.weight}g"

    @property
    def formatted_packing(self):
        if not self.packing_options:
            return ""
        
        val = self.packing_options.strip()
        weight_str = f"{float(self.weight):g}"
        
        if '/' in val:
            # Legacy format (e.g. 100/50)
            val_parts = [p.strip() for p in val.split('/', 1)]
            if len(val_parts) == 2:
                return f"{val_parts[0]}g/{val_parts[1]}pcs"
                
        # New format (e.g. 50) -> pulls weight automatically
        return f"{weight_str}g/{val}pcs"

    def clean(self):
        super().clean()
        if self.is_active and not self.barcode:
            raise ValidationError({'barcode': 'Barcode is required to activate the product option.'})

    def save(self, *args, **kwargs):
        self.clean()
        if self.image:
            if not self.image.name.lower().endswith('.webp'):
                self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

class HeroBanner(models.Model):
    PLACEMENT_CHOICES = [
        ('HOME', 'Homepage'),
        ('BLOG_LIST', 'Blog List Page'),
        ('BLOG_POST', 'Blog Post Inner Page'),
        ('PARTNERS', 'Partners Page'),
        ('PRODUCTS', 'Products List Page'),
        ('ABOUT', 'About Us Page'),
        ('CAREERS', 'Careers Page'),
        ('CONTACT', 'Contact Page'),
    ]
    
    title = HTMLField(blank=True, help_text="Текст заголовка (можно форматировать)")
    subtitle = HTMLField(blank=True, help_text="Текст подзаголовка под главным заголовком")
    show_text_overlay = models.BooleanField(default=True, help_text="Показывать заголовок и подзаголовок поверх баннера")
    
    placement = models.CharField(max_length=50, choices=PLACEMENT_CHOICES, default='HOME', help_text="Where this banner should be displayed")
    
    image = models.ImageField(upload_to='banners/', null=True, blank=True, help_text="Desktop Banner image. Рекомендуемый размер: 1920x300 пикселей.")
    image_mobile = models.ImageField(upload_to='banners/mobile/', null=True, blank=True, help_text="Mobile Banner image (Vertical). Рекомендуемый размер: 1080x1920 пикселей.")
    
    video_file = models.FileField(upload_to='banners/videos/', null=True, blank=True, help_text="Upload .mp4 or .webm for animated Desktop banners. Overrides image.")
    video_file_mobile = models.FileField(upload_to='banners/videos/mobile/', null=True, blank=True, help_text="Upload .mp4 or .webm for animated Mobile banners. Overrides mobile image.")
    banner_link = models.URLField(blank=True, help_text="Optional link when clicking the banner")
    is_active = models.BooleanField(default=True)
    show_on_mobile = models.BooleanField(default=True, help_text="Show this banner on mobile devices")
    show_on_desktop = models.BooleanField(default=False, help_text="Show this banner on PC/large screens")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Banners'
        ordering = ['order', '-id']

    def __str__(self):
        return self.title or f"Banner {self.id}"

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.lower().endswith(('.webp', '.gif', '.svg')):
            self.image = optimize_image(self.image)
        super().save(*args, **kwargs)
