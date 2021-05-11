from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Products, DealerTransaction, CustomerTransaction
from dealers.models import Dealers
from CustomerManagement.models import Customer
from django.contrib import messages
from .forms import IssueForm, ReceiveForm
from datetime import datetime,date 
from django.template.loader import get_template, render_to_string
from .utils import render_to_pdf 
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

# Create your views here.

def display_products(request):
    products = Products.objects.all()
    context = {'products':products}

    return render(request, 'product_list.htm', context)

def create(request):
    if request.method=="POST":
        get_category = request.POST['category']
        get_item = request.POST['item']
        get_quantity = request.POST['quantity']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        get_company = request.POST['company']
        get_address = request.POST['address']
        get_email_address = request.POST['email_address']
        get_phone = request.POST['phone']
        get_mfdate = request.POST['mfdate']
        get_expdate = request.POST['expdate']
        get_dealer_status = request.POST.get('dealer-status', False); 
        get_rate = request.POST['rate']
        get_amount = request.POST['amount'] 
        get_paid_amount = request.POST['paid-amount']
        products = Products(category=get_category, item_name=get_item, quantity=get_quantity, received_date=get_mfdate, expiry_date=get_expdate, rate=get_rate, amount=get_amount)
        products.save() 
        
        if get_dealer_status != False:
            dealers = Dealers(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone, added_date=date.today())
            
            duplicates = Dealers.objects.filter(phone=get_phone)
            
            if duplicates.count()==0:
                dealers.save()
                products.dealer.set = Dealers(dealers.id)
                products.save()
                dealer_tran = DealerTransaction(total_amount=get_amount, date=date.today(),paid_amount=get_paid_amount)
                dealer_tran.dealer=Dealers(dealers.id)
                dealer_tran.product=Products(products.id)
                dealer_tran.remaining_due=int(float(dealer_tran.total_amount)) - int(float(dealer_tran.paid_amount))
                dealer_tran.save()
            elif (duplicates[0].added_date <= dealers.added_date):
                
                dealers.save()
                dealers.delete()
                products.dealer.set = Dealers(duplicates[0].id)
                products.save()
                dealer_tran = DealerTransaction(total_amount=get_amount, date=date.today(),paid_amount=get_paid_amount)
                dealer_tran.dealer=Dealers(duplicates[0].id)
                dealer_tran.product=Products(products.id)
                dealer_tran.remaining_due=int(float(dealer_tran.total_amount)) - int(float(dealer_tran.paid_amount))
                dealer_tran.save()                
                            
        print("Data inserted successfully!!")
        
    return render(request, 'product_add.htm')

def product_sell_to_customer(request, id):
    product = Products.objects.get(id=id)
    if request.method == "POST":
        get_item = request.POST['item']
        get_quantity = request.POST['quantity']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        get_company = request.POST['company']
        get_address = request.POST['address']
        get_email_address = request.POST['email_address']
        get_phone = request.POST['phone']
        get_rate = request.POST['rate']
        get_amount = request.POST['amount'] 
        get_paid_amount = request.POST['paid-amount']

        customers = Customer(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone, added_date=date.today())
        
        duplicates = Customer.objects.filter(phone=get_phone)
        if duplicates.count()==0:
            customers.save()
            product.customer.set = Customer(customers.id)
            product.quantity = int(product.quantity) - int(get_quantity)
            product.save()
            customer_tran = CustomerTransaction(total_amount=get_amount, date=date.today(),paid_amount=get_paid_amount,quantity=get_quantity)
            customer_tran.customer=Customer(customers.id)
            customer_tran.product=Products(product.id)
            customer_tran.remaining_due=int(float(customer_tran.total_amount)) - int(float(customer_tran.paid_amount))
            customer_tran.save()
        elif (duplicates[0].added_date <= customers.added_date):
            print("You are already registered!!!")
            customers.save()
            customers.delete()
            product.customer.set = Customer(duplicates[0].id)
            product.quantity = int(product.quantity) - int(get_quantity)
            product.save()
            customer_tran = CustomerTransaction(total_amount=get_amount, date=date.today(),paid_amount=get_paid_amount,quantity=get_quantity)
            customer_tran.customer=Customer(duplicates[0].id)
            customer_tran.product=Products(product.id)
            customer_tran.remaining_due=int(float(customer_tran.total_amount)) - int(float(customer_tran.paid_amount))
            customer_tran.save()

    return redirect('/products')

def delete(request, id):
    product = Products.objects.get(id=id)
    product.delete()
    print("Deleted successfully!!")
    return redirect('/products')   


def product_detail(request, pk):
    queryset = Products.objects.get(id=pk)
	
    context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	
    return render(request, "product_detail.htm", context)


def transactions(request):
    dealer = DealerTransaction.objects.all()
    customer = CustomerTransaction.objects.all()
    context = {'dealer':dealer, 'customer':customer}
    return render(request, "transactions.htm", context)

def product_sell(request,pk):
    queryset = Products.objects.get(id=pk)
	
    context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
    return render(request, "product_sell.htm", context)

def update_transaction(request, id):
    queryset = DealerTransaction.objects.get(id=id)
    
    if request.method=="POST":
        get_total = request.POST['amount']
        get_paid_amount = request.POST['paid-amount']

        queryset.total_amount=get_total
        queryset.paid_amount=get_paid_amount
        queryset.remaining_due=int(float(queryset.total_amount))-int(float(queryset.paid_amount))
        queryset.save()
        
    print(queryset.remaining_due)
    return redirect('/transactions')

def update(request, id):
    queryset = DealerTransaction.objects.get(id=id)
    
    context = {
        "queryset": queryset,
        
    }
    return render(request, "update_transaction.htm", context)

def update_customer(request, id):
    customerset = CustomerTransaction.objects.get(id=id)
    context={
        "customerset": customerset
    }
    return render(request, "update_transaction_c.htm", context)

def update_customer_transaction(request, id):
    customerset = CustomerTransaction.objects.get(id=id)    
    if request.method=="POST":
        get_total = request.POST['amount']
        get_paid_amount = request.POST['paid-amount']

        customerset.total_amount=get_total
        customerset.paid_amount=get_paid_amount
        customerset.remaining_due=int(float(customerset.total_amount))-int(float(customerset.paid_amount))
        customerset.save()
        
    return redirect('/transactions')

def receipt_form(request):
    return render(request, "receipt_form.htm")

def print_receipt_customer(request, id):
    queryset = CustomerTransaction.objects.get(id=id)
    vatrate = 0.07
    vat=queryset.total_amount + queryset.total_amount*vatrate
    context = {
        "queryset":queryset,
        "get_vat":vat
    }

    return render(request, "receipt_form.htm", context)
