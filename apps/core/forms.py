from django import forms

class PartnershipForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=100, required=False)
    company_name = forms.CharField(max_length=200, required=False)
    phone = forms.CharField(max_length=50, required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)
