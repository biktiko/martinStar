import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

INSTALLED_APPS = [
    'modeltranslation',
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'storages',
    
    # Local apps
    'apps.users',
    'apps.catalog',
    'apps.orders',
    'apps.core',
    'apps.blog',
    
    # Third-party apps
    'django_editorjs_fields',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Analytics middleware
    'apps.analytics.middleware.AmplitudeMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

db_url = env('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
if "?pgbouncer=true" in db_url:
    db_url = db_url.replace("?pgbouncer=true", "")

db_config = environ.Env.db_url_config(db_url)
db_config['CONN_MAX_AGE'] = 60
db_config['CONN_HEALTH_CHECKS'] = True

DATABASES = {
    'default': db_config
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'martin-star-cache',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'hy'

LANGUAGES = (
    ('hy', 'Armenian'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Anymail / Email settings
ANYMAIL = {}
if env('RESEND_API_KEY', default=''):
    ANYMAIL['RESEND_API_KEY'] = env('RESEND_API_KEY')
    EMAIL_BACKEND = 'anymail.backends.resend.EmailBackend'
elif env('SENDGRID_API_KEY', default=''):
    ANYMAIL['SENDGRID_API_KEY'] = env('SENDGRID_API_KEY')
    EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
elif env('MAILGUN_API_KEY', default=''):
    ANYMAIL['MAILGUN_API_KEY'] = env('MAILGUN_API_KEY')
    ANYMAIL['MAILGUN_SENDER_DOMAIN'] = env('MAILGUN_SENDER_DOMAIN', default='')
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
elif env('MAILJET_API_KEY', default=''):
    ANYMAIL['MAILJET_API_KEY'] = env('MAILJET_API_KEY')
    ANYMAIL['MAILJET_SECRET_KEY'] = env('MAILJET_SECRET_KEY', default='')
    EMAIL_BACKEND = 'anymail.backends.mailjet.EmailBackend'
else:
    EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_TIMEOUT = env.int('EMAIL_TIMEOUT', default=10)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'width': 'auto',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen insertdatetime nonbreaking
        contextmenu directionality searchreplace wordcount visualblocks
        visualchars code fullscreen autolink lists charmap print hr
        anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# Amplitude Analytics
AMPLITUDE_API_KEY = env('AMPLITUDE_API_KEY', default='')

# Supabase Storage / S3 configuration
if env.bool('USE_S3', default=True) or env('BUCKET_ACCESS_KEY', default=None):
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    AWS_ACCESS_KEY_ID = env('BUCKET_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = env('BUCKET_SECRET_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
    AWS_S3_REGION_NAME = 'eu-central-1'
    AWS_S3_ADDRESSING_STYLE = 'path'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    
    # Let django-storages build the URL correctly for Supabase public access
    supabase_url = env('SUPABASE_URL', default='')
    if supabase_url:
        supabase_domain = supabase_url.replace('https://', '').replace('http://', '')
    else:
        # Fallback to extracting from S3 endpoint
        supabase_domain = AWS_S3_ENDPOINT_URL.split('//')[1].split('/')[0].replace('.storage.', '.')
        
    AWS_S3_CUSTOM_DOMAIN = f"{supabase_domain}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"

else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
