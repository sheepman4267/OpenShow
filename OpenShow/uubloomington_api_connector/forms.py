from django import forms


class CreateShowFromOOSForm(forms.Form):
    order_of_service_id = forms.CharField(max_length=9000, label='Order of Service Page ID')
