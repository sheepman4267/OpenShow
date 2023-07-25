from django import forms

class CreateShowFromOOSForm(forms.Form):
    order_of_service_url = forms.CharField(max_length=9000, label='Order of Service API URL')
