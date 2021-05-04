from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=254)
    phone = PhoneNumberField()
    added_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.firstname
    

