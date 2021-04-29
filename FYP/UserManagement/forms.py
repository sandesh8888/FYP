from django import forms
from django.contrib.auth.models import User
from FYP.UserManagement.models import AdminProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ('username','email','password')

class AdminProfileInfo(forms.ModelForm):
    class Meta():
        models = AdminProfileInfo
        fields = ('profile_pic')