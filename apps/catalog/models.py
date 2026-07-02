from django.db import models
from apps.core.image_optimization import optimize_image

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
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

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    # FMCG specific
    ingredients = models.TextField(blank=True)
    nutritional_value = models.TextField(blank=True, help_text="e.g., Calories: 200, Protein: 5g")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight in grams")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    image = models.ImageField(upload_to='products/')
    
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
            # Check if it's a new upload or has been modified.
            # Simplified approach: if the image file name doesn't end in .webp, convert it.
            if not self.image.name.lower().endswith('.webp'):
                self.image = optimize_image(self.image)
        super().save(*args, **kwargs)
