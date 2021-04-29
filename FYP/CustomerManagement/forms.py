from django import forms
from .models import Customer
#DataFlair
class CustomerCreate(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'