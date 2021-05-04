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

# Create your views here.

def dashboard(request):
    dealers = Dealers.objects.all().count()
    customers = Customer.objects.all().count()
    products = Products.objects.order_by().values('item_name').distinct().count()
    recent_dealer = Dealers.objects.filter(added_date=date.today()).count()
    recent_customer = Customer.objects.filter(added_date=date.today()).count()
    oldest_dealer = Dealers.objects.earliest('added_date')
    oldest_customer = Customer.objects.earliest('added_date')
    top_product = CustomerTransaction.objects.values('product').annotate(dcount=Count('product'))
    print(top_product)
    context={
        'dealers': dealers,
        'customers':customers,
        'products': products,
        'recent_dealer':recent_dealer,
        'recent_customer':recent_customer,
        'oldest_dealer':oldest_dealer,
        'oldest_customer':oldest_customer,
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
        
        print("Data inserted successfully!!")
        redirect('/customer')

    return render(request, 'customer_management/customer_form.htm')


def delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    print("Deleted successfully!!")
    return redirect('/customer')


