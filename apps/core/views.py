from django.shortcuts import render
from django.views.decorators.cache import cache_page
from apps.core.models import SiteSettings, CompanyHistory, PartnerLogo, ExportCountry, BranchOffice, Vacancy
from apps.blog.models import Post
from apps.core.forms import PartnershipForm
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator
from apps.catalog.models import Category, HeroBanner

@cache_page(60 * 15)
def index(request):
    categories = Category.objects.filter(is_active=True).order_by('id')
    
    paginator = Paginator(categories, 6)
    page_number = request.GET.get('page')
    categories_page = paginator.get_page(page_number)
    
    active_banners = HeroBanner.objects.filter(is_active=True, placement='HOME')
    mobile_banners = [b for b in active_banners if b.show_on_mobile]
    desktop_banners = [b for b in active_banners if b.show_on_desktop]
    
    favourite_posts = Post.objects.filter(is_favourite=True, is_active=True).select_related('topic').order_by('-created_at')[:3]
        
    context = {
        'categories': categories_page,
        'mobile_banners': mobile_banners,
        'desktop_banners': desktop_banners,
        'favourite_posts': favourite_posts,
        'settings': SiteSettings.load(),
    }
    return render(request, 'index.html', context)

def about(request):
    history_milestones = CompanyHistory.objects.filter(is_active=True).order_by('year')
    banner = HeroBanner.objects.filter(placement='ABOUT', is_active=True).first()
    context = {
        'history_milestones': history_milestones,
        'banner': banner,
    }
    return render(request, 'about.html', context)

def partnership_view(request):
    if request.method == 'POST':
        form = PartnershipForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Construct email content
            subject = f"New Partnership Request from {data['first_name']} {data['last_name']}"
            body = f"""
            New Partnership Request:
            
            Name: {data['first_name']} {data['last_name']}
            Email: {data['email']}
            Phone: {data.get('phone', 'N/A')}
            City: {data.get('city', 'N/A')}
            Company Name: {data.get('company_name', 'N/A')}
            
            Comment:
            {data.get('comment', 'N/A')}
            """
            
            try:
                email = EmailMessage(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else [settings.DEFAULT_FROM_EMAIL],
                    cc=['marketing@martinstar.am']
                )
                email.send(fail_silently=False)
                return JsonResponse({"status": "success"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    # GET request
    banner = HeroBanner.objects.filter(placement='PARTNERSHIP', is_active=True).first()
    partner_logos = PartnerLogo.objects.filter(is_active=True)
    export_countries = ExportCountry.objects.filter(is_active=True)
    
    # Format export_countries as a dictionary for the template JS
    # e.g. {'RU': 'Россия: Москва, Санкт-Петербург', 'AM': 'Армения: Ереван'}
    countries_data = {}
    active_country_codes = []
    for c in export_countries:
        active_country_codes.append(c.map_code)
        countries_data[c.map_code] = c.name

    context = {
        'banner': banner,
        'partner_logos': partner_logos,
        'countries_data': countries_data,
        'active_country_codes': active_country_codes,
        'global_settings': SiteSettings.load(),
    }
    return render(request, 'partnership.html', context)

def contacts_view(request):
    hq = BranchOffice.objects.filter(is_headquarters=True).first()
    branches = BranchOffice.objects.filter(is_headquarters=False).order_by('order')
    
    context = {
        'hq': hq,
        'branches': branches,
    }
    return render(request, 'contacts.html', context)

def careers_view(request):
    vacancies = Vacancy.objects.filter(is_active=True).order_by('order', 'id')
    context = {
        'vacancies': vacancies,
    }
    return render(request, 'careers.html', context)

def apply_job_view(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
    
    try:
        name = request.POST.get('name') or request.GET.get('name', '')
        phone = request.POST.get('phone') or request.GET.get('phone', '')
        email = request.POST.get('email') or request.GET.get('email', '')
        message = request.POST.get('message') or request.GET.get('message', '')
        vacancy_title = request.POST.get('vacancy_title') or request.GET.get('vacancy_title', '')
        cv_file = request.FILES.get('cv_file')

        settings_obj = SiteSettings.load()
        
        to_email = settings_obj.hr_email if settings_obj.hr_email else 'hr@martinstar.am'
        cc_emails = [e.strip() for e in settings_obj.hr_cc_emails.split(',')] if settings_obj.hr_cc_emails else []
        cc_emails = [e for e in cc_emails if e] # remove empty strings

        subject = f"New Job Application: {vacancy_title}"
        body = f"""
        New Job Application for: {vacancy_title}
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        
        Message:
        {message}
        """

        email_msg = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            cc=cc_emails
        )
        if cv_file:
            email_msg.attach(cv_file.name, cv_file.read(), cv_file.content_type)
            
        email_msg.send(fail_silently=True)
        return JsonResponse({"status": "success"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e) or repr(e)}, status=500)
