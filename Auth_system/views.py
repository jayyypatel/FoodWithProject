from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from Auth_system.models import CustomUser
from .forms import loginUser, registerUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from manager_app.models import Restaurant_manager
from django.conf import settings
#
from django.utils.safestring import mark_safe
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

#
# Create your views here.
def loginpage(request):
    return render(request,'Auth_system/login.html')

def register(request):
    return render(request,'Auth_system/register.html') # return register page 

def register_user(request): # used to register user in system
    form = registerUser()
    if request.method == 'POST':
        form = registerUser(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('Auth_system:login_user_n') #loginpage
            
        else:
            messages.info(request,mark_safe('1. Email must be in format like tmp@gmail.com <br/>2. Password Contains at list 8 character, alphabets and specials'))
            return render(request,'Auth_system/registernew.html',{'form':form})
    
    return render(request,'Auth_system/registernew.html',{'form':form}) #registernew.html

def login_user(request):
    #here it is form for login user
    form = loginUser()
    err = 0
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(request,username=username,password = password)
        
        if user is not None:
            login(request, user) # login with username and password
            #it will check role for user
            if request.user.user_choice == 'customer':
                return redirect('root:index')
            elif request.user.user_choice == 'manager':
                if Restaurant_manager.objects.filter(user_fk = request.user.id).exists():
                    return redirect('manager_app:dashboard')
                else:
                    return redirect('manager_app:regi_rest')
            else:
                pass
        else:
            messages.error(request,'Username or Password not correct')
            return render(request,'Auth_system/login.html',{'form':form})
    return render(request, 'Auth_system/login.html',{'form':form})

def tmp(request):
    return render(request,'Auth_system/tmp.html')

@login_required(login_url='Auth_system:login_user_n')  
def logout_user(request):
    logout(request)
    
    
    return redirect('Auth_system:login_user_n')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "Auth_system/password_reset.txt"
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
                        
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
                    
					return redirect("Auth_system:password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="Auth_system/password_reset.html", context={"password_reset_form":password_reset_form})