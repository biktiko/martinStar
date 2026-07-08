import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.core.models import CompanyHistory

CompanyHistory.objects.all().delete()

milestones = [
    (2007, 'Company Foundation', 'Martin Star started as a small business producing roasted seeds.', 'about/history/2007.jpg'),
    (2009, 'Early Growth', 'Expanded product lines and entered local retail markets.', 'about/history/2009.jpg'),
    (2010, 'Facility Expansion', 'Opened a new manufacturing facility to meet growing demand.', 'about/history/2010.jpg'),
    (2013, 'National Distribution', 'Achieved nationwide distribution across major supermarket chains.', 'about/history/2013.jpg'),
    (2021, 'Modernization', 'Upgraded equipment for automated, high-volume production.', 'about/history/2021.jpg'),
    (2022, 'International Export', 'Began exporting products to neighboring countries.', 'about/history/2022.jpg'),
    (2024, 'Global Brand', 'Established presence in over 70 countries worldwide.', 'about/history/2024.jpg')
]

for i, (y, t, d, img) in enumerate(milestones):
    m = CompanyHistory.objects.create(year=y, title=t, description=d, image=img, order=i)
    # Set translations
    m.title_ru = t
    m.title_en = t
    m.title_hy = t
    m.description_ru = d
    m.description_en = d
    m.description_hy = d
    m.save()

print('Added', len(milestones), 'milestones with images.')
