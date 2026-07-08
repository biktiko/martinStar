import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.core.models import CompanyHistory
for milestone in CompanyHistory.objects.all():
    milestone.title_hy = milestone.title
    milestone.title_ru = milestone.title
    milestone.title_en = milestone.title
    milestone.description_hy = milestone.description
    milestone.description_ru = milestone.description
    milestone.description_en = milestone.description
    milestone.save()
print('Updated translations.')
