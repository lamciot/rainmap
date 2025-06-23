from django import forms
from . import models

class MxMap (forms.ModelForm):
    class Meta:
        model = models.MuongXen
        fields = ['date_time','data']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data': forms.Textarea()
        }
        
class DateTimeSearchForm(forms.Form):
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '3600'}),
        label='Select Date and Time'
    )

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)