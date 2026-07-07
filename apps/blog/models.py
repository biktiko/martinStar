from django.db import models
from django_editorjs_fields import EditorJsJSONField
from django.urls import reverse
from django.utils import timezone

class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    
    # Block editor field (stores JSON)
    body = EditorJsJSONField(
        plugins=[
            "@editorjs/paragraph",
            "@editorjs/header",
            "@editorjs/image",
            "@editorjs/embed",
            "@editorjs/list",
            "@editorjs/marker",
        ],
        null=True,
        blank=True,
    )
    
    cover_image = models.ImageField(upload_to='blog/covers/', null=True, blank=True)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_favourite = models.BooleanField(default=False, help_text="Pin this post to the homepage")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Auto-fill empty translations from the default language (hy)
        # so the user doesn't have to rebuild the block layout with images
        
        def is_empty_body(val):
            if not val:
                return True
            if isinstance(val, dict):
                return not val.get('blocks')
            if isinstance(val, str):
                import json
                try:
                    parsed = json.loads(val)
                    return not parsed.get('blocks')
                except:
                    return True
            return False

        if hasattr(self, 'body_hy') and not is_empty_body(self.body_hy):
            if hasattr(self, 'body_en') and is_empty_body(self.body_en):
                self.body_en = self.body_hy
            if hasattr(self, 'body_ru') and is_empty_body(self.body_ru):
                self.body_ru = self.body_hy
                
        super().save(*args, **kwargs)
