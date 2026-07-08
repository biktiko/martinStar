import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.core.models import CompanyHistory
CompanyHistory.objects.all().delete()
CompanyHistory.objects.create(year=2008, title='Company Foundation', description='Martin Star started as a small business producing roasted seeds.', order=1)
CompanyHistory.objects.create(year=2012, title='First Major Expansion', description='Expanded operations to a larger facility and began producing a wider variety of snacks.', order=2)
CompanyHistory.objects.create(year=2018, title='International Markets', description='Started exporting products to over 10 countries globally.', order=3)
CompanyHistory.objects.create(year=2026, title='Modern Holding', description='Grown into a powerful holding with 200+ commodity items and operations in 70+ countries.', order=4)
print('Added 4 milestones.')
