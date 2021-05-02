from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Products, DealerTransaction, CustomerTransaction
from dealers.models import Dealers
from django.contrib import messages
from .forms import IssueForm, ReceiveForm
import datetime
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
            dealers = Dealers(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone)
            dealers.save()
            products.dealer = Dealers(dealers.id)
            products.save()
            dealer_tran = DealerTransaction(total_amount=get_amount, date=datetime.date.today(),paid_amount=get_paid_amount)
            dealer_tran.dealer=Dealers(dealers.id)
            dealer_tran.product=Products(products.id)
            dealer_tran.remaining_due=int(dealer_tran.total_amount) - int(dealer_tran.paid_amount)
            dealer_tran.save()
        
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


def transactions(request):
    dealer = DealerTransaction.objects.all()
    context = {'dealer':dealer}
    return render(request, "transactions.htm", context)

