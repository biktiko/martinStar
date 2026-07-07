from modeltranslation.translator import register, TranslationOptions
from .models import Post, Topic

@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'body')
