from django.db import models
from dealers.models import Dealers
from CustomerManagement.models import Customer

# Create your models here.
class Products(models.Model):
        item_name = models.CharField(max_length=50, blank=True, null=True)
        category = models.CharField(max_length=50, blank=True, null=True)
        quantity = models.IntegerField(default='0', blank=True, null=True)
        rate = models.FloatField(blank=False,null=False)
        vat = 0.13
        amount = models.FloatField(blank=False,null=False)
        receive_quantity = models.IntegerField(default='0', blank=True, null=True)
        received_date = models.DateTimeField(blank=True, null=True)
        expiry_date = models.DateTimeField(blank=True, null=True)
        dealer = models.ForeignKey(Dealers, on_delete=models.CASCADE, blank=True, null=True)
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
        issue_quantity = models.IntegerField(default='0', blank=True, null=True)
        reorder_level = models.IntegerField(default='0', blank=True, null=True)
        last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
        

        def __str__(self):
            return self.item_name


class DealerTransaction(models.Model):
    dealer = models.ForeignKey(Dealers, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    


