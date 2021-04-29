from django import forms
from .models import Products
from dealers.models import Dealers
from CustomerManagement.models import Customer

class IssueForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['issue_quantity','customer']
		
class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['receive_quantity','dealer']

       