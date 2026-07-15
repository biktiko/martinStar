from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label=_("First Name"))
    last_name = forms.CharField(max_length=30, required=False, label=_("Last Name"))
    email = forms.EmailField(required=True, label=_("Email"))
    phone_number = forms.CharField(max_length=20, required=False, label=_("Phone Number (Optional)"))
    password = forms.CharField(widget=forms.PasswordInput, required=True, label=_("Password"))
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label=_("Confirm Password"))
    newsletter_optin = forms.BooleanField(required=False, label=_("Subscribe to our newsletter"))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(_("Passwords don't match."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                newsletter_optin=self.cleaned_data.get("newsletter_optin", False)
            )
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput, required=True, label=_("Password"))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(_("Invalid email or password."))
            self.user = user
            
        return cleaned_data
