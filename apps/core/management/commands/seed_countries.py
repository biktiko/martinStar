from django.core.management.base import BaseCommand
from apps.core.models import ExportCountry

class Command(BaseCommand):
    help = 'Seeds the database with export countries'

    def handle(self, *args, **kwargs):
        data = {
            'Australia': [
                ('Австралия', 'AU'),
                ('Новая Зеландия', 'NZ')
            ],
            'Asia': [
                ('Армения', 'AM'), ('Бахрейн', 'BH'), ('Вьетнам', 'VN'), ('Грузия', 'GE'), 
                ('Израиль', 'IL'), ('Индонезия', 'ID'), ('Иордания', 'JO'), ('Казахстан', 'KZ'), 
                ('Катар', 'QA'), ('Кипр', 'CY'), ('Киргизия', 'KG'), ('Китай', 'CN'), 
                ('Кувейт', 'KW'), ('Монголия', 'MN'), ('ОАЭ', 'AE'), ('Сингапур', 'SG'), 
                ('Сирия', 'SY'), ('Таджикистан', 'TJ'), ('Тайланд', 'TH'), ('Туркмения', 'TM'), 
                ('Турция', 'TR'), ('Узбекистан', 'UZ'), ('Южная Корея', 'KR'), ('Япония', 'JP')
            ],
            'North America': [
                ('Канада', 'CA'), ('Куба', 'CU'), ('Мексика', 'MX'), ('США', 'US')
            ],
            'Africa': [
                ('Алжир', 'DZ'), ('Египет', 'EG'), ('Ливия', 'LY'), 
                ('Марокко', 'MA'), ('Тунис', 'TN'), ('ЮАР', 'ZA')
            ],
            'Europe': [
                ('Австрия', 'AT'), ('Англия', 'GB'), ('Белоруссия', 'BY'), ('Бельгия', 'BE'), 
                ('Болгария', 'BG'), ('Босния и Герцеговина', 'BA'), ('Венгрия', 'HU'), 
                ('Германия', 'DE'), ('Греция', 'GR'), ('Дания', 'DK'), ('Исландия', 'IS'), 
                ('Испания', 'ES'), ('Италия', 'IT'), ('Латвия', 'LV'), ('Литва', 'LT'), 
                ('Мальта', 'MT'), ('Молдавия', 'MD'), ('Нидерланды', 'NL'), ('Норвегия', 'NO'), 
                ('Польша', 'PL'), ('Португалия', 'PT'), ('Россия', 'RU'), ('Румыния', 'RO'), 
                ('Словакия', 'SK'), ('Словения', 'SI'), ('Туркменистан', 'TM'), ('Украина', 'UA'), 
                ('Финляндия', 'FI'), ('Франция', 'FR'), ('Хорватия', 'HR'), ('Черногория', 'ME'), 
                ('Чехия', 'CZ'), ('Швеция', 'SE'), ('Эстония', 'EE')
            ]
        }

        # Clear existing if any
        ExportCountry.objects.all().delete()
        self.stdout.write("Deleted existing ExportCountries")

        for region, countries in data.items():
            for name, code in countries:
                # Avoid duplicate Turkmenistan
                if not ExportCountry.objects.filter(map_code=code).exists():
                    ExportCountry.objects.create(name=name, map_code=code, region=region)
                    self.stdout.write(f"Added {name} ({code}) to {region}")

        self.stdout.write(self.style.SUCCESS("Migration completed successfully!"))
