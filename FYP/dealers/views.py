from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Dealers
import datetime

# Create your views here.

def display_dealers(request):
    dealers = Dealers.objects.all()
    context = {'dealers':dealers}

    return render(request, 'dealers/dealer_list.htm', context)


def create(request):
    if request.method=="POST":

        fname = request.POST['firstname']
        lname = request.POST['lastname']
        get_company = request.POST['company']
        get_address = request.POST['address']
        get_email_address = request.POST['email_address']
        get_phone = request.POST['phone']
   
        dealers = Dealers(firstname=fname, lastname=lname, company=get_company, address=get_address, email_address=get_email_address, phone=get_phone, added_date=datetime.date.today())       
        duplicates = Dealers.objects.filter(phone=get_phone)
        if duplicates.count()==0:
            dealers.save()
        elif (duplicates[0].added_date <= dealers.added_date):
            print("You are already registered!!!")
            dealers.save()
            dealers.delete()
        print("Data inserted successfully!!")
        redirect('/dealer')

    return render(request, 'dealers/dealer_form.htm')

def delete(request, id):
    dealer = Dealers.objects.get(id=id)
    dealer.delete()
    print("Deleted successfully!!")
    return redirect('/dealer')