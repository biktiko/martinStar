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
    'Items in the assortment': {'ru': 'Товаров в ассортименте', 'hy': 'Ապրանքներ տեսականիում', 'en': 'Items in the assortment'},
    'Partnership': {'ru': 'Партнерство', 'hy': 'Համագործակցություն', 'en': 'Partnership'},
    'Logistics': {'ru': 'Логистика', 'hy': 'Լոգիստիկա', 'en': 'Logistics'},
    'ОТЛАЖЕННЫЕ ПРОЦЕССЫ': {'ru': 'ОТЛАЖЕННЫЕ ПРОЦЕССЫ', 'hy': 'ԿԱՐԳԱՎՈՐՎԱԾ ԳՈՐԾԸՆԹԱՑՆԵՐ', 'en': 'SMOOTH PROCESSES'},
    'Для качественного и своевременного обеспечения партнеров продукцией компании мы создали логистический центр. Наличие собственной складской базы позволяет комплектовать необходимые объемы поставок, а современный парк автомобильного транспорта обеспечивает своевременную адресную доставку.': {
        'ru': 'Для качественного и своевременного обеспечения партнеров продукцией компании мы создали логистический центр. Наличие собственной складской базы позволяет комплектовать необходимые объемы поставок, а современный парк автомобильного транспорта обеспечивает своевременную адресную доставку.',
        'hy': 'Ընկերության արտադրանքով գործընկերներին որակյալ և ժամանակին ապահովելու համար մենք ստեղծել ենք լոգիստիկ կենտրոն։ Սեփական պահեստային բազայի առկայությունը թույլ է տալիս կոմպլեկտավորել անհրաժեշտ մատակարարումների ծավալները, իսկ ավտոմոբիլային տրանսպորտի ժամանակակից պարկը ապահովում է ժամանակին հասցեական առաքում։',
        'en': 'To ensure high-quality and timely supply of our company’s products to our partners, we have created a logistics center. Having our own warehouse base allows us to complete the necessary delivery volumes, and a modern fleet of vehicles ensures timely targeted delivery.'
    },
    'Become a Partner': {'ru': 'Стать Партнером', 'hy': 'Դառնալ Գործընկեր', 'en': 'Become a Partner'},
    'Fill out the form below and our managers will contact you.': {'ru': 'Заполните форму ниже, и наши менеджеры свяжутся с вами.', 'hy': 'Լրացրեք ստորև բերված ձևը և մեր մենեջերները կկապվեն ձեզ հետ:', 'en': 'Fill out the form below and our managers will contact you.'},
    'They Work With Us': {'ru': 'Они Работают С Нами', 'hy': 'Նրանք Աշխատում Են Մեզ Հետ', 'en': 'They Work With Us'},
    'Supply Countries': {'ru': 'Страны Поставок', 'hy': 'Մատակարարման Երկրներ', 'en': 'Supply Countries'},
    'Join the Team': {'ru': 'Присоединяйтесь к команде', 'hy': 'Միացեք թիմին', 'en': 'Join the Team'},
    'Employees': {'ru': 'Сотрудников', 'hy': 'Աշխատակիցներ', 'en': 'Employees'},
    'We Offer': {'ru': 'Мы предлагаем', 'hy': 'Մենք առաջարկում ենք', 'en': 'We Offer'},
    'Stability & Growth': {'ru': 'Стабильность и рост', 'hy': 'Կայունություն և աճ', 'en': 'Stability & Growth'},
    'A reliable workplace in an international company with continuous opportunities for professional growth.': {'ru': 'Надежное рабочее место в международной компании с постоянными возможностями для профессионального роста.', 'hy': 'Հուսալի աշխատատեղ միջազգային ընկերությունում՝ մասնագիտական աճի շարունակական հնարավորություններով։', 'en': 'A reliable workplace in an international company with continuous opportunities for professional growth.'},
    'Modern Resources': {'ru': 'Современные ресурсы', 'hy': 'Ժամանակակից ռեսուրսներ', 'en': 'Modern Resources'},
    'Access to cutting-edge tools, modern facilities, and a comfortable working environment.': {'ru': 'Доступ к передовым инструментам, современным объектам и комфортной рабочей среде.', 'hy': 'Հասանելիություն առաջադեմ գործիքներին, ժամանակակից հարմարություններին և հարմարավետ աշխատանքային միջավայրին։', 'en': 'Access to cutting-edge tools, modern facilities, and a comfortable working environment.'},
    'Competitive Benefits': {'ru': 'Конкурентные преимущества', 'hy': 'Մրցակցային առավելություններ', 'en': 'Competitive Benefits'},
    'Attractive salary packages, health resources, and performance-based bonuses.': {'ru': 'Привлекательные зарплатные пакеты, ресурсы для здоровья и бонусы по результатам работы.', 'hy': 'Գրավիչ աշխատավարձային փաթեթներ, առողջության ապահովագրություն և աշխատանքի արդյունքների վրա հիմնված բոնուսներ։', 'en': 'Attractive salary packages, health resources, and performance-based bonuses.'},
    'We Look For': {'ru': 'Мы ищем', 'hy': 'Մենք փնտրում ենք', 'en': 'We Look For'},
    'Ambition & Drive': {'ru': 'Амбициозность и целеустремленность', 'hy': 'Հավակնոտություն և նպատակասլացություն', 'en': 'Ambition & Drive'},
    'Professionals who are eager to achieve results and take ownership of their projects.': {'ru': 'Профессионалы, стремящиеся к достижению результатов и берущие на себя ответственность за свои проекты.', 'hy': 'Մասնագետներ, ովքեր ձգտում են հասնել արդյունքների և պատասխանատվություն են կրում իրենց նախագծերի համար։', 'en': 'Professionals who are eager to achieve results and take ownership of their projects.'},
    'Team Collaboration': {'ru': 'Командное сотрудничество', 'hy': 'Թիմային համագործակցություն', 'en': 'Team Collaboration'},
    'Strong communicators who thrive in cross-functional teams and value mutual respect.': {'ru': 'Отличные коммуникаторы, которые процветают в кросс-функциональных командах и ценят взаимное уважение.', 'hy': 'Ուժեղ հաղորդակցման հմտություններ ունեցողներ, ովքեր հաջողում են խաչաձև գործառութային թիմերում և գնահատում են փոխադարձ հարգանքը։', 'en': 'Strong communicators who thrive in cross-functional teams and value mutual respect.'},
    'Problem Solving': {'ru': 'Решение проблем', 'hy': 'Խնդիրների լուծում', 'en': 'Problem Solving'},
    'Innovative thinkers who can overcome challenges and continuously improve processes.': {'ru': 'Новаторы, которые могут преодолевать трудности и постоянно улучшать процессы.', 'hy': 'Նորարար մտածողներ, ովքեր կարող են հաղթահարել մարտահրավերները և անընդհատ բարելավել գործընթացները։', 'en': 'Innovative thinkers who can overcome challenges and continuously improve processes.'},
    'Open Positions': {'ru': 'Открытые вакансии', 'hy': 'Թափուր հաստիքներ', 'en': 'Open Positions'},
    'There are currently no open positions. However, you can still send us your CV!': {'ru': 'В настоящее время нет открытых вакансий. Однако вы все равно можете отправить нам свое резюме!', 'hy': 'Ներկայումս բաց հաստիքներ չկան։ Այնուամենայնիվ, դուք կարող եք ուղարկել մեզ ձեր ինքնակենսագրականը։', 'en': 'There are currently no open positions. However, you can still send us your CV!'},
    'Send CV': {'ru': 'Отправить резюме', 'hy': 'Ուղարկել ինքնակենսագրականը', 'en': 'Send CV'},
    'Apply Now': {'ru': 'Подать заявку', 'hy': 'Դիմել հիմա', 'en': 'Apply Now'},
    'Apply for': {'ru': 'Подача заявки на', 'hy': 'Դիմում՝', 'en': 'Apply for'},
    'Full Name *': {'ru': 'Полное имя *', 'hy': 'Անուն Ազգանուն *', 'en': 'Full Name *'},
    'Phone *': {'ru': 'Телефон *', 'hy': 'Հեռախոս *', 'en': 'Phone *'},
    'Email *': {'ru': 'Email *', 'hy': 'Էլ․ փոստ *', 'en': 'Email *'},
    'Attach CV / Portfolio *': {'ru': 'Прикрепить резюме / портфолио *', 'hy': 'Կցել ինքնակենսագրական / պորտֆոլիո *', 'en': 'Attach CV / Portfolio *'},
    'Cover Letter / Message': {'ru': 'Сопроводительное письмо', 'hy': 'Ուղեկցող նամակ', 'en': 'Cover Letter'},
    'Submit Application': {'ru': 'Отправить заявку', 'hy': 'Ուղարկել դիմումը', 'en': 'Submit Application'},
    'Sending...': {'ru': 'Отправка...', 'hy': 'Ուղարկվում է...', 'en': 'Sending...'},
    'An error occurred. Please try again.': {'ru': 'Произошла ошибка. Пожалуйста, попробуйте еще раз.', 'hy': 'Տեղի է ունեցել սխալ։ Խնդրում ենք կրկին փորձել։', 'en': 'An error occurred. Please try again.'},
    'Network error. Please try again.': {'ru': 'Ошибка сети. Пожалуйста, попробуйте еще раз.', 'hy': 'Ցանցի սխալ։ Խնդրում ենք կրկին փորձել։', 'en': 'Network error. Please try again.'},
    'Application Sent!': {'ru': 'Заявка отправлена!', 'hy': 'Դիմումն ուղարկված է։', 'en': 'Application Sent!'},
    'Thank you for your interest. Our HR team will review your application and contact you soon.': {'ru': 'Спасибо за ваш интерес. Наша HR-команда рассмотрит вашу заявку и скоро свяжется с вами.', 'hy': 'Շնորհակալություն հետաքրքրության համար։ Մեր ՄՌ բաժինը կքննարկի ձեր դիմումը և շուտով կկապվի ձեզ հետ։', 'en': 'Thank you for your interest. Our HR team will review your application and contact you soon.'},
    'Close': {'ru': 'Закрыть', 'hy': 'Փակել', 'en': 'Close'},
    'Brands': {'ru': 'Бренды', 'hy': 'Բրենդներ', 'en': 'Brands'},
    'Login': {'ru': 'Вход', 'hy': 'Մուտք', 'en': 'Login'},
    'Register': {'ru': 'Регистрация', 'hy': 'Գրանցում', 'en': 'Register'},
    'Welcome Back': {'ru': 'С возвращением', 'hy': 'Բարի վերադարձ', 'en': 'Welcome Back'},
    "Don't have an account?": {'ru': 'Нет аккаунта?', 'hy': 'Չունե՞ք հաշիվ', 'en': "Don't have an account?"},
    'Sign up': {'ru': 'Зарегистрироваться', 'hy': 'Գրանցվել', 'en': 'Sign up'},
    'Sign in': {'ru': 'Войти', 'hy': 'Մուտք գործել', 'en': 'Sign in'},
    'Why log in?': {'ru': 'Зачем входить?', 'hy': 'Ինչու՞ մուտք գործել', 'en': 'Why log in?'},
    'Create an Account Now': {'ru': 'Создать аккаунт', 'hy': 'Ստեղծել հաշիվ', 'en': 'Create an Account Now'},
    'Create an Account': {'ru': 'Создать аккаунт', 'hy': 'Ստեղծել հաշիվ', 'en': 'Create an Account'},
    'Already have an account?': {'ru': 'Уже есть аккаунт?', 'hy': 'Արդեն ունե՞ք հաշիվ', 'en': 'Already have an account?'},
    'Please correct the following errors:': {'ru': 'Пожалуйста, исправьте следующие ошибки:', 'hy': 'Խնդրում ենք ուղղել հետևյալ սխալները:', 'en': 'Please correct the following errors:'},
    'Subscribe to our newsletter': {'ru': 'Подписаться на новости', 'hy': 'Բաժանորդագրվել նորություններին', 'en': 'Subscribe to our newsletter'},
    'Возможность получения новостей на почту': {'ru': 'Возможность получения новостей на почту', 'hy': 'Նորություններ ստանալու հնարավորություն', 'en': 'Opportunity to receive news by email'},
    'Более персонализированный и быстрый подход в поддержке': {'ru': 'Более персонализированный и быстрый подход в поддержке', 'hy': 'Ավելի անհատականացված և արագ աջակցություն', 'en': 'A more personalized and faster approach to support'},
    'By registering, you get a': {'ru': 'Регистрируясь, вы получаете', 'hy': 'Գրանցվելով՝ դուք ստանում եք', 'en': 'By registering, you get a'},
    'Log out': {'ru': 'Выйти', 'hy': 'Դուրս գալ', 'en': 'Log out'},
    'About Us': {'ru': 'О нас', 'hy': 'Մեր մասին', 'en': 'About Us'},
    'Over the years of existence, from a small business producing roasted seeds, our company has grown into a powerful holding that implements all stages of a complex agricultural production process: from growing in our own fields to selling quality products on store shelves.': {
        'ru': 'За годы существования из небольшого предприятия по производству жареных семечек наша компания выросла в мощный холдинг, реализующий все этапы сложного сельскохозяйственного производственного процесса: от выращивания на собственных полях до реализации качественной продукции на полках магазинов.',
        'hy': 'Գոյության տարիների ընթացքում բոված արևածաղկի արտադրության փոքր ձեռնարկությունից մեր ընկերությունը վերածվել է հզոր հոլդինգի, որն իրականացնում է բարդ գյուղատնտեսական արտադրական գործընթացի բոլոր փուլերը՝ սեփական դաշտերում աճեցումից մինչև խանութների դարակներում որակյալ արտադրանքի վաճառք։',
        'en': 'Over the years of existence, from a small business producing roasted seeds, our company has grown into a powerful holding that implements all stages of a complex agricultural production process: from growing in our own fields to selling quality products on store shelves.'
    },
    'Years on the market': {'ru': 'Лет на рынке', 'hy': 'Տարիներ շուկայում', 'en': 'Years on the market'},
    'Countries': {'ru': 'Стран', 'hy': 'Երկրներ', 'en': 'Countries'},
    'Commodity Items': {'ru': 'Товарных позиций', 'hy': 'Ապրանքատեսակներ', 'en': 'Commodity Items'},
    'Our Advantages': {'ru': 'Наши преимущества', 'hy': 'Մեր առավելությունները', 'en': 'Our Advantages'},
    'Customer confidence': {'ru': 'Доверие потребителей', 'hy': 'Սպառողների վստահությունը', 'en': 'Customer confidence'},
    'We strive to create healthy and natural products for our clients all over the world, we try to satisfy their needs and exceed expectations.': {
        'ru': 'Мы стремимся создавать здоровые и натуральные продукты для наших клиентов по всему миру, стараемся удовлетворить их потребности и превзойти ожидания.',
        'hy': 'Մենք ձգտում ենք ստեղծել առողջ և բնական արտադրանք մեր հաճախորդների համար ամբողջ աշխարհում, փորձում ենք բավարարել նրանց կարիքները և գերազանցել սպասումները։',
        'en': 'We strive to create healthy and natural products for our clients all over the world, we try to satisfy their needs and exceed expectations.'
    },
    'Own raw materials': {'ru': 'Собственное сырье', 'hy': 'Սեփական հումք', 'en': 'Own raw materials'},
    'An important advantage of the holding is the availability of its own agricultural land, processing base, warehouses.': {
        'ru': 'Важным преимуществом холдинга является наличие собственных сельскохозяйственных угодий, перерабатывающей базы, складов.',
        'hy': 'Հոլդինգի կարևոր առավելություններից է սեփական գյուղատնտեսական հողատարածքների, վերամշակող բազայի և պահեստների առկայությունը։',
        'en': 'An important advantage of the holding is the availability of its own agricultural land, processing base, warehouses.'
    },
    'Technological production': {'ru': 'Технологичное производство', 'hy': 'Տեխնոլոգիական արտադրություն', 'en': 'Technological production'},
    'Constant updating of the technical base allows achieving high quality products and uninterrupted production cycle.': {
        'ru': 'Постоянное обновление технической базы позволяет добиваться высокого качества продукции и бесперебойного производственного цикла.',
        'hy': 'Տեխնիկական բազայի անընդհատ նորացումը թույլ է տալիս հասնել բարձրորակ արտադրանքի և անխափան արտադրական ցիկլի։',
        'en': 'Constant updating of the technical base allows achieving high quality products and uninterrupted production cycle.'
    },
    'Quality control': {'ru': 'Контроль качества', 'hy': 'Որակի վերահսկողություն', 'en': 'Quality control'},
    'All enterprises have modern quality control laboratories operating at all stages, from raw materials to final products.': {
        'ru': 'На всех предприятиях работают современные лаборатории контроля качества на всех этапах, от сырья до готовой продукции.',
        'hy': 'Բոլոր ձեռնարկություններն ունեն ժամանակակից որակի վերահսկման լաբորատորիաներ, որոնք գործում են բոլոր փուլերում՝ հումքից մինչև վերջնական արտադրանք։',
        'en': 'All enterprises have modern quality control laboratories operating at all stages, from raw materials to final products.'
    },
    'Our History': {'ru': 'Наша история', 'hy': 'Մեր պատմությունը', 'en': 'Our History'},
    'Quality raw materials': {'ru': 'Качественное сырье', 'hy': 'Որակյալ հումք', 'en': 'Quality raw materials'},
    'Striving for higher standards': {'ru': 'Стремление к высоким стандартам', 'hy': 'Ձգտում դեպի բարձր չափանիշներ', 'en': 'Striving for higher standards'},
    'Always High Quality': {'ru': 'Всегда высокое качество', 'hy': 'Միշտ բարձր որակ', 'en': 'Always High Quality'},
    'To meet the highest expectations, we process thousands of tons of selected raw materials. Strict adherence to international standards and non-stop quality control guarantees that every product reaching your table delivers genuine taste and nutritional value. The company\'s goal is to establish long-term, mutually beneficial cooperation built on an impeccable reputation.': {
        'ru': 'Чтобы соответствовать самым высоким ожиданиям, мы перерабатываем тысячи тонн отборного сырья. Строгое соблюдение международных стандартов и безостановочный контроль качества гарантируют, что каждый продукт, попадающий на ваш стол, обладает подлинным вкусом и пищевой ценностью. Цель компании - установление долгосрочного, взаимовыгодного сотрудничества, основанного на безупречной репутации.',
        'hy': 'Ամենաբարձր սպասումներին համապատասխանելու համար մենք վերամշակում ենք հազարավոր տոննա ընտրված հումք: Միջազգային ստանդարտների խիստ պահպանումը և անդադար որակի վերահսկումը երաշխավորում են, որ ձեր սեղանին հասնող յուրաքանչյուր արտադրանքն ունի իսկական համ և սննդային արժեք: Ընկերության նպատակն է ստեղծել երկարաժամկետ, փոխշահավետ համագործակցություն՝ հիմնված անբասիր հեղինակության վրա:',
        'en': 'To meet the highest expectations, we process thousands of tons of selected raw materials. Strict adherence to international standards and non-stop quality control guarantees that every product reaching your table delivers genuine taste and nutritional value. The company\'s goal is to establish long-term, mutually beneficial cooperation built on an impeccable reputation.'
    },
}

@register.simple_tag(takes_context=True)
def t(context, text):
    """
    Simple translation tag for static templates without gettext .mo files.
    """
    lang = getattr(context.get('request'), 'LANGUAGE_CODE', 'hy')
    return TRANSLATIONS.get(text, {}).get(lang, text)

@register.filter(name='split')
def split(value, key):
    """
    Returns the value turned into a list, stripping whitespace.
    """
    return [v.strip() for v in value.split(key)]

