from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'

    def ready(self):
        # Monkey patch EditorJsWidget to ignore form_class passed by modeltranslation
        from django_editorjs_fields.widgets import EditorJsWidget
        original_init = EditorJsWidget.__init__
        
        def patched_init(self, plugins=None, tools=None, config=None, **kwargs):
            kwargs.pop('form_class', None)
            
            # Unfold admin injects its own widget which lacks these attributes
            widget = kwargs.get('widget')
            if widget and not hasattr(widget, 'plugins'):
                kwargs.pop('widget')
                
            original_init(self, plugins=plugins, tools=tools, config=config, **kwargs)
            
        EditorJsWidget.__init__ = patched_init
