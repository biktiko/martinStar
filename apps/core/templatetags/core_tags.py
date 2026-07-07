from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang_code):
    """
    Returns the URL for the current page in the specified language.
    Handles the prefix_default_language=False behavior by manually replacing prefixes.
    """
    request = context['request']
    path = request.path
    
    # Strip the current language prefix if it exists
    for code, name in settings.LANGUAGES:
        prefix = f'/{code}/'
        if path.startswith(prefix):
            path = path[len(prefix) - 1:] # Leave the leading slash
            break
            
    # Add the new language prefix
    if lang_code != settings.LANGUAGE_CODE:
        # Other languages get the prefix
        path = f'/{lang_code}{path}'
        
    query_string = request.META.get('QUERY_STRING', '')
    if query_string:
        path = f"{path}?{query_string}"
        
    return path

TRANSLATIONS = {
    'Home': {'ru': 'Главная', 'hy': 'Գլխավոր', 'en': 'Home'},
    'About us': {'ru': 'О нас', 'hy': 'Մեր մասին', 'en': 'About us'},
    'Products': {'ru': 'Продукция', 'hy': 'Արտադրանք', 'en': 'Products'},
    'Careers': {'ru': 'Карьера', 'hy': 'Կարիերա', 'en': 'Careers'},
    'Contacts': {'ru': 'Контакты', 'hy': 'Կապ', 'en': 'Contacts'},
    'Online store': {'ru': 'Интернет-магазин', 'hy': 'Առցանց խանութ', 'en': 'Online store'},
    'Blog': {'ru': 'Блог', 'hy': 'Բլոգ', 'en': 'Blog'},
    'Search products...': {'ru': 'Поиск товаров...', 'hy': 'Որոնել...', 'en': 'Search products...'},
    'Company': {'ru': 'Компания', 'hy': 'Ընկերություն', 'en': 'Company'},
    'Privacy Policy': {'ru': 'Политика конфиденциальности', 'hy': 'Գաղտնիության քաղաքականություն', 'en': 'Privacy Policy'},
    'Our Products': {'ru': 'Наша продукция', 'hy': 'Մեր արտադրանքը', 'en': 'Our Products'},
    'Toggle filter': {'ru': 'Переключить фильтр', 'hy': 'Փոխել ֆիլտրը', 'en': 'Toggle filter'},
    'No image': {'ru': 'Нет фото', 'hy': 'Նկար չկա', 'en': 'No image'},
    'No Image': {'ru': 'Нет фото', 'hy': 'Նկար չկա', 'en': 'No Image'},
    'No categories found.': {'ru': 'Категории не найдены.', 'hy': 'Կատեգորիաներ չեն գտնվել:', 'en': 'No categories found.'},
    'No products found': {'ru': 'Товары не найдены', 'hy': 'Ապրանքներ չեն գտնվել', 'en': 'No products found'},
    'Try selecting a different brand or category.': {'ru': 'Попробуйте выбрать другой бренд или категорию.', 'hy': 'Փորձեք ընտրել այլ ապրանքանիշ կամ կատեգորիա:', 'en': 'Try selecting a different brand or category.'},
    'No Image Available': {'ru': 'Нет фото', 'hy': 'Նկար չկա', 'en': 'No Image Available'},
    'Select Weight': {'ru': 'Выберите вес', 'hy': 'Ընտրեք քաշը', 'en': 'Select Weight'},
    'g': {'ru': 'г', 'hy': 'գ', 'en': 'g'},
    'Specifications': {'ru': 'Характеристики', 'hy': 'Բնութագրեր', 'en': 'Specifications'},
    'Barcode': {'ru': 'Штрихкод', 'hy': 'Շտրիխ կոդ', 'en': 'Barcode'},
    'L x W x H': {'ru': 'Д х Ш х В', 'hy': 'Ե x Լ x Բ', 'en': 'L x W x H'},
    'Packing': {'ru': 'Упаковка', 'hy': 'Փաթեթավորում', 'en': 'Packing'},
    'Shelf Life': {'ru': 'Срок годности', 'hy': 'Պահպանման ժամկետ', 'en': 'Shelf Life'},
    'days': {'ru': 'дней', 'hy': 'օր', 'en': 'days'},
    'Minimum storage temperature': {'ru': 'Мин. температура хранения', 'hy': 'Պահպանման նվազագույն ջերմաստիճան', 'en': 'Minimum storage temperature'},
    'Maximum storage temperature': {'ru': 'Макс. температура хранения', 'hy': 'Պահպանման առավելագույն ջերմաստիճան', 'en': 'Maximum storage temperature'},
    'Nutrition Value': {'ru': 'Пищевая ценность', 'hy': 'Սննդային արժեք', 'en': 'Nutrition Value'},
    'Nutritional Value per 100g': {'ru': 'Пищевая ценность на 100г', 'hy': 'Սննդային արժեք 100գ-ում', 'en': 'Nutritional Value per 100g'},
    'Energy': {'ru': 'Энергия', 'hy': 'Էներգիա', 'en': 'Energy'},
    'Proteins': {'ru': 'Белки', 'hy': 'Սպիտակուցներ', 'en': 'Proteins'},
    'Fats': {'ru': 'Жиры', 'hy': 'Ճարպեր', 'en': 'Fats'},
    'Carbs': {'ru': 'Углеводы', 'hy': 'Ածխաջրեր', 'en': 'Carbs'},
    'Positions': {'ru': 'Позиций', 'hy': 'Ապրանքատեսակներ', 'en': 'Positions'},
    'Categories': {'ru': 'Категорий', 'hy': 'Կատեգորիաներ', 'en': 'Categories'},
    'All': {'ru': 'Все', 'hy': 'Բոլորը', 'en': 'All'},
}

@register.simple_tag(takes_context=True)
def t(context, text):
    """
    Simple translation tag for static templates without gettext .mo files.
    """
    lang = getattr(context.get('request'), 'LANGUAGE_CODE', 'hy')
    return TRANSLATIONS.get(text, {}).get(lang, text)

