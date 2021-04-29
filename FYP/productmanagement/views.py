from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Products
from dealers.models import Dealers
from django.contrib import messages 
from .forms import IssueForm, ReceiveForm
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
        get_dealer_radio = request.POST['flexRadioDefault']  
        get_rate = request.POST['rate']
        get_amount = request.POST['amount'] 
        products = Products(category=get_category, item_name=get_item, quantity=get_quantity, received_date=get_mfdate, expiry_date=get_expdate, rate=get_rate, amount=get_amount)
        products.save() 
        
        if get_dealer_radio == "on":
            dealers = Dealers(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone)
            dealers.save()
            products.dealer = Dealers(dealers.id)
            products.save()
        
        print("Data inserted successfully!!")
        
    return render(request, 'product_add.htm')


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

