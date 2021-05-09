from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerCreate
from django.views.generic import ListView
import datetime
from django.db.models import Count
from productmanagement.models import Products, DealerTransaction, CustomerTransaction
from dealers.models import Dealers
from datetime import date
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Max

# Create your views here.

def dashboard(request):
    dealers = Dealers.objects.all().count()
    customers = Customer.objects.all().count()
    products = Products.objects.order_by().values('item_name').distinct().count()
    recent_dealer = Dealers.objects.filter(added_date=date.today()).count()
    recent_customer = Customer.objects.filter(added_date=date.today()).count()
    oldest_dealer = Dealers.objects.earliest('added_date')
    oldest_customer = Customer.objects.earliest('added_date')
    top_product_list = CustomerTransaction.objects.filter().values('product').annotate(dcount=Count('product'))
    
    total_paid_dealer = DealerTransaction.objects.aggregate(Sum('paid_amount'))
    total_paid_customer = CustomerTransaction.objects.aggregate(Sum('paid_amount'))
    total_remaining_dealer = DealerTransaction.objects.aggregate(Sum('remaining_due'))
    total_remaining_customer = CustomerTransaction.objects.aggregate(Sum('remaining_due'))
    top_product=list(map(lambda x : x['product'], top_product_list))

    print(top_product_list)

    print(Products.objects.get(id=top_product[0]))
    transaction_by_date = CustomerTransaction.objects.filter().values('product_id').annotate(data_sum=Sum('paid_amount'))
    date_dict = list(map(lambda x : x['product_id'], transaction_by_date))
    data_dict = list(map(lambda x : x['data_sum'], transaction_by_date))
    
    context={
        'dealers': dealers,
        'customers':customers,
        'products': products,
        'recent_dealer':recent_dealer,
        'recent_customer':recent_customer,
        'oldest_dealer':oldest_dealer,
        'oldest_customer':oldest_customer,
        'total_paid_dealer':total_paid_dealer,
        'total_paid_customer':total_paid_customer,
        'total_remaining_dealer':total_remaining_dealer,
        'total_remaining_customer':total_remaining_customer,
        'labels':date_dict,
        'data':data_dict,
        'top_product':Products.objects.get(id=top_product[0]),

    }
    
    return render(request, "customer_management/dashboard.htm", context)


def display_customers(request):
    customer = Customer.objects.all()
    context = {'customer':customer}

    return render(request, 'customer_management/customer_list.htm', context)

#CRUD operations
def create(request):
    if request.method=="POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        get_company = request.POST['company']
        get_address = request.POST['address']
        get_email_address = request.POST['email_address']
        get_phone = request.POST['phone']

        customer = Customer(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone, added_date=datetime.date.today())       
        duplicates = Customer.objects.filter(phone=get_phone)
        print(duplicates)
        if duplicates.count()==0:
            customer.save()
        elif (duplicates[0].added_date <= customer.added_date):  
            print("You are already registered!!!") 
            customer.save()         
            customer.delete()
        messages.success(request, "Customer added successfully")
        print("Data inserted successfully!!")
        redirect('/customer')

    return render(request, 'customer_management/customer_form.htm')


def delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    messages.success(request, "Customer deleted successfully")
    print("Deleted successfully!!")
    return redirect('/customer')


