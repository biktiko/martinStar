from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from .models import Post, Topic

@admin.register(Topic)
class TopicAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(ModelAdmin, TranslationAdmin):
    list_display = ('title', 'topic', 'is_active', 'is_favourite', 'created_at', 'updated_at')
    list_select_related = ('topic',)
    list_editable = ('is_active', 'is_favourite', 'topic')
    list_filter = ('topic', 'is_active', 'is_favourite', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
