from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def special(request):
    return HttpResponse("You are logged in")

def password_reset(request):
    return render(request, 'usermanagement/password_reset_form.htm')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('/dashboard/')
            else:
                return HttpResponse("Account not active")
        else:
            print("Tresspassers !!!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request,'usermanagement/login.htm',{})

def display_home(request):
    return render(request, 'usermanagement/home.htm')
