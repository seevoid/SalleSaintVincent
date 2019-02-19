from django import forms

PRESTA_CHOICES= [
    ('fete', 'Fete'),
    ('pro', 'Pro'),
    ]

class resaForm(forms.Form):
    name_resa = forms.CharField(required=True)
    email_resa = forms.EmailField(required=True)
    phone_number_resa = forms.CharField(required=True) 
    message_resa = forms.CharField(required=True) 
    optradio = forms.CharField(required=False)
    dates_resa = forms.CharField(required=False)

class contactForm(forms.Form):
    name_contact = forms.CharField(required=True)
    email_contact = forms.EmailField(required=True)
    phone_number_contact = forms.CharField(required=False) 
    message_contact = forms.CharField(required=True) 

