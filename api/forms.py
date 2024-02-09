from django import forms

class ContactForm(forms.Form):
    url = forms.URLField(label='URL', initial='http://innerflect.com')
    name_company = forms.CharField(label='Company', initial='Inner Flect')
    first_name = forms.CharField(label='First Name', initial='John')
    last_name = forms.CharField(label='Last Name', initial='Doe')
    email = forms.EmailField(label='Email Address', initial='john@example.com')
    accept_terms = forms.BooleanField(label='I accept the terms and conditions', initial=True, required=False)
