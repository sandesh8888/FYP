from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerCreate
from django.views.generic import ListView

# Create your views here.

def dashboard(request):
    return render(request, "customer_management/dashboard.htm")


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
            
        customer = Customer(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone)
        customer.save()
        print("Data inserted successfully!!")
        redirect('/customer')

    return render(request, 'customer_management/customer_form.htm')


def delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    print("Deleted successfully!!")
    return redirect('/customer')