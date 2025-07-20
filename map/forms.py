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
    username = forms.CharField(required = True)
    password = forms.CharField()

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    retype_password = forms.CharField(required=True)
    
class EditForm(forms.Form):
    # date_time= forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '3600'})
    st_xala= forms.IntegerField()
    st_muonglat= forms.IntegerField()
    st_cuadat= forms.IntegerField()
    st_quychau= forms.IntegerField()
    st_muongxen= forms.IntegerField()
    # confirm_ow = forms.BooleanField(required=False)
#    cancel_ow = forms.BooleanField()
    
    def save(self, instance=None):
        if instance:
            # Update existing instance
            instance.st_xa_la = self.cleaned_data['st_xala']
            instance.st_muong_lat = self.cleaned_data['st_muonglat']
            instance.st_cua_dat = self.cleaned_data['st_cuadat']
            instance.st_quy_chau = self.cleaned_data['st_quychau']
            instance.st_muong_xen = self.cleaned_data['st_muongxen']
            instance.save()
        else:
            print("No instance")
        #     # Create new instance
        #     instance = models.MuongXen(
        #         st_xa_la=self.cleaned_data['st_xa_la'],
        #         st_muong_lat=self.cleaned_data['st_muong_lat'],
        #         st_cua_dat=self.cleaned_data['st_cua_dat'],
        #         st_quy_chau=self.cleaned_data['st_quy_chau'],
        #         st_muong_xen=self.cleaned_data['st_muong_xen'],
        #     )
        
        return instance
# class EditForm(forms.ModelForm):
#     class Meta:
#         model = models.MuongXen
#         fields = ['st_xa_la','st_muong_lat','st_cua_dat','st_quy_chau','st_muong_xen']
#         # widgets = {
#         #     'st_xala': forms.IntegerField(),
#         #     'st_muonglat': forms.IntegerField(),
#         #     'st_cuadat': forms.IntegerField(),
#         #     'st_quychau': forms.IntegerField(),
#         #     'st_muongxen': forms.IntegerField()
#         # }