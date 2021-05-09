from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

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
            messages.error(request, "Invalid Login Details")
            return render(request,'usermanagement/login.htm')
            
    else:
        return render(request,'usermanagement/login.htm',{})

def display_home(request):
    return render(request, 'usermanagement/home.htm')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "usermanagement/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("/")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    
    return render(request=request, template_name="usermanagement/password_reset_form.htm", context={"password_reset_form":password_reset_form})
