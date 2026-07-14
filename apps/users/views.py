from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.http import require_POST
from django.conf import settings
from .forms import RegistrationForm, LoginForm
from .models import CustomUser

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verify_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = _("Verify your email - Martin Star")
    message = _("Please click the link below to verify your email address:\n\n") + verify_url
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            messages.success(request, _("Registration successful! Please check your email to verify your account."))
            return redirect('login')
    else:
        form = RegistrationForm()
        
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            if not user.is_email_verified:
                messages.warning(request, _("Please verify your email address before logging in."))
                # Optionally resend email here
            else:
                login(request, user)
                messages.success(request, _("Successfully logged in."))
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
    else:
        form = LoginForm()
        
    return render(request, 'users/login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect('index')

def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(request, _("Your email has been verified! You can now log in."))
        return redirect('login')
    else:
        messages.error(request, _("The verification link is invalid or has expired."))
        return redirect('login')
