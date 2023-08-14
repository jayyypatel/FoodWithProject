from datetime import datetime
from http.client import HTTPResponse
from django.contrib import messages 
from django.core.mail import send_mail,BadHeaderError
from django.shortcuts import redirect
from django.shortcuts import render
from restaurant.models  import Category, Product, Restaurant
import random
import socket
from django.conf import settings
from root.forms import EmailForm
from smtplib import SMTPAuthenticationError,SMTPException
# Create your views here.

def index(request):
    products = list(Product.objects.all())

    top_dicount_products = Product.objects.order_by('-discount')[:3]#goes to choose and enjoy page for top 3 discount 
    
    product_popular = random.sample(products,3)     
    
    product_4 = Product.objects.all()[:4]           # only 4 products in index page have to make it more realibable
    
    sing_restaurant = Restaurant.objects.get(id=5)  #for last of the page to display one restaurant
    sing_rest_pro = Product.objects.filter(restaurant_fk=sing_restaurant)[:3]

    
    context={
        'top_dicount_pro':top_dicount_products,
        'product_popular':product_popular,
        'product_4':product_4,
        'sing_restaurant':sing_restaurant,
        'sing_rest_pro':sing_rest_pro

    }
    return render(request,'root/index.html',context)

def contactus(request):
    form = EmailForm()
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        
        if form.is_valid():
            to_mail = form.cleaned_data.get('email_id')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            form.save()
            
            #reply as email to contected person
            try:
                
                send_mail('Your Query is recevied',
                        'Thank you for your response....',#message
                        settings.EMAIL_HOST_USER,
                        [to_mail],
                        fail_silently= False
                        )
            except ConnectionError as e: 
                print('There is an Authentication Error',e)
            except SMTPException as e :
                print('There was error in sending email:  ' , e)
            
            
            try:
                send_mail(subject,
                        f'from: {to_mail} {message}',#message
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],
                        fail_silently= False
                        )
            except SMTPException as e :
                print('There was error in sending error:  ' , e)
            
                

            messages.warning(request,'We will reach you soon')
            return redirect('root:contactus')
            
    context ={
        'form':form
    }
    return render(request,'root/contactus.html',context=context)

def aboutus(request):
    
    return render(request,'root/aboutus.html')

# def choose_enjoy(request):
#     products = Product.objects.all()[:3]
#     context={
#         'product_enj':products
#     }
#     return render(request,'root/section_choose_enjoy.html',context)




def popular_this_month(request):
    pass