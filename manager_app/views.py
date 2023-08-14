from datetime import datetime
from itertools import count, product
from math import fabs
from multiprocessing import context
import re
from socket import MsgFlag
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import request
from django.shortcuts import redirect, render
from Auth_system.models import CustomUser
from manager_app.forms import manager_Form, product_Form
from manager_app.models import Restaurant_manager
from manager_app.utils import pdf
from restaurant.forms import  address_registerForm, booking_Form, category_registerForm, rating_Form, rest_registerForm, tbl_Form
from restaurant.models import Address, Book_with_order, Booking, Category, Order, Order_details, Product, Rating, Restaurant, Table, booking_details
from django.core.mail import send_mail
from django.conf import settings


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.loader import get_template
from weasyprint import HTML

import os
from django.db.models import Sum

# Create your views here.
def dashboard(request):
    user = CustomUser.objects.get(pk = request.user.id)
    rest = Restaurant_manager.objects.get(user_fk=user)

    pro_cnt = Product.objects.filter(restaurant_fk=rest.restaurant_fk).count()
    tbl_cnt = Table.objects.filter(restaurant_fk = rest.restaurant_fk ).count()
    revenue1 = Booking.objects.filter(restaurant_fk=rest.restaurant_fk).aggregate(Sum('total_price'))
    
    
    
    context={
        'user':user,
        'rest' : rest,
        'pro_cnt':pro_cnt,
        'tbl_cnt':tbl_cnt,
        'revenue':revenue1['total_price__sum']
    }
    return render(request,'manager_app/index.html',context)

def food_items(request):
    user = CustomUser.objects.get(pk = request.user.id)
    rest = Restaurant_manager.objects.get(user_fk=user)

    all_product = Product.objects.filter(restaurant_fk=rest.restaurant_fk)
    context = {
            'all_product':all_product
    }
    return render(request,'manager_app/food_items.html',context)

def confirmation(request,id):
    b_obj = Booking.objects.get(pk=id)
    user = CustomUser.objects.get(pk=b_obj.user_id.id)
    
    send_mail('Your Booking has been Confirmed',
            'please check your user profile on website and you can download invoice',#message
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently= False
        )

    b_obj.confirm = True
    b_obj.save()
    return redirect('manager_app:dashboard')

#order with table book
def orderlist(request):
    cdate = datetime.now()
    user = CustomUser.objects.get(pk=request.user.id)
    rest = Restaurant_manager.objects.get(user_fk=user)
    
    up_fwt_booking = Booking.objects.filter(booking_type='dine-in',restaurant_fk=rest.restaurant_fk,date__gte=cdate).order_by('date')
    past_fwt_booking = Booking.objects.filter(booking_type='dine-in',restaurant_fk=rest.restaurant_fk,date__lt=cdate)
    #for table name
    up_booking_details = booking_details.objects.filter(booking_fk__in=up_fwt_booking)
    past_booking_details = booking_details.objects.filter(booking_fk__in=past_fwt_booking)
    print(up_fwt_booking)
    print(past_fwt_booking)
    print(Booking.objects.filter(booking_type='dine-in',restaurant_fk=rest.restaurant_fk).count())
    context={
        'fwt_booking':up_fwt_booking,
        'up_booking_details':up_booking_details,
        'past_fwt_booking':past_fwt_booking,
        'past_booking_details':past_booking_details
    }
    return render(request,'manager_app/order-list.html',context)

#this is for particular order details like id 1 order contains 4 items pizza , burger, ...
def pr_order_details(request,bid):
    book_obj = Booking.objects.get(pk=bid)
    bworder_obj = Book_with_order.objects.get(booking_id=book_obj)
    
    #used to access order details one by one
    order_details = Order_details.objects.filter(order_fk=bworder_obj.order_id)
    
    orderdetails_total = 0
    for i in order_details:
        orderdetails_total += i.quantity * i.product_fk.price
    final_total = orderdetails_total + book_obj.total_price
    
    context={
        'order_details':order_details,
        'bworder_obj':bworder_obj,
        'orderdetails_total':orderdetails_total,
        'final_total':final_total

    }
    return render(request,'manager_app/pr_order.html',context)


#for register restaurants
def register_rest(request):
    print('heelo')
    rest_form = rest_registerForm()
    add_form = address_registerForm()
    cat_form = category_registerForm()
    rat_form = rating_Form()
    
    print('after')
    if request.method == 'POST':
        
        print('heelo')

        rest_form = rest_registerForm(request.POST, request.FILES)
        add_form = address_registerForm(request.POST)
        cat_form = category_registerForm(request.POST)
        rat_form = rating_Form(request.POST)
        
        
        if add_form.is_valid():
            add_form.save()
        add_last = Address.objects.latest('id')

        if cat_form.is_valid():
            cat_form.save()
        cat_last = Category.objects.latest('id')

        if rat_form.is_valid():
            rat_form.save()
        rat_last = Rating.objects.latest('id')    

        if rest_form.is_valid():
            rest_form = rest_form.save(commit=False)
            rest_form.rating_fk = rat_last
            rest_form.address_fk = add_last
            rest_form.category_fk = cat_last
            rest_form.save()
            
            rest_last = Restaurant.objects.latest('id')
            print(rest_last.id)
            ##############################here
            man_form = manager_Form()
            man_form = man_form.save(commit=False)
            
            user = CustomUser.objects.get(pk = request.user.id)
            man_form.user_fk = user
            man_form.restaurant_fk = rest_last
            man_form.save()

            return redirect('manager_app:dashboard')
        
    
    
    context = {
            'rest_form':rest_form,
            'cat_form':cat_form,
            'add_form':add_form,
            'rat_form':rat_form,
            

        
    }
    return render(request,'manager_app/rest_register.html',context)


def register_pro(request):
    form = product_Form()
    if request.method == 'POST':
        form = product_Form(request.POST,request.FILES)

        if form.is_valid():
            user = CustomUser.objects.get(pk = request.user.id)
            rest = Restaurant_manager.objects.get(user_fk=user)
            form = form.save(commit=False)
            form.restaurant_fk = rest.restaurant_fk
            form.save()
            return redirect('manager_app:food_items')
    context = {
        'form':form
    }
    return render(request,'manager_app/product_regi.html',context)

def register_tbl(request):
    user = CustomUser.objects.get(pk = request.user.id)
    rest = Restaurant_manager.objects.get(user_fk=user)

    form = tbl_Form()
    if request.method == 'POST':
        form = tbl_Form(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.restaurant_fk = rest.restaurant_fk
            form.save()
            messages.success(request, 'Table added successfully..')
            return HttpResponseRedirect(request.path_info)
            
    context = {
        'form':form,
        
    }
    return render(request,'manager_app/tbl.html',context)

def tbl_details(request):
    user = CustomUser.objects.get(pk = request.user.id)
    rest = Restaurant_manager.objects.get(user_fk=user)
    all_tables = Table.objects.filter(restaurant_fk=rest.restaurant_fk)
    context={
        'all_tables':all_tables
    }
    return render(request,'manager_app/tbl_details.html',context)

#delete table from manager side
def del_tbl(request,tbl_id):
    tbl = Table.objects.get(pk=tbl_id)
    tbl.delete()
    return redirect('manager_app:tbl_details')

# def bookings(request):
#     user = CustomUser.objects.get(pk = request.user.id)
#     rest = Restaurant_manager.objects.get(user_fk=user)

#     all_bookings = Booking.objects.filter(restaurant_fk=rest.restaurant_fk,booking_type='none')
#     all_booking_details = booking_details.objects.filter(booking_fk__in=all_bookings)
#     print(all_bookings)
#     context = {
#         'all_bookings':all_bookings,
#         'all_booking_details':all_booking_details
#     }
#     return render(request,'manager_app/bookings.html',context)




def upcomming_booking(request):
    cdate = datetime.now()
    user = CustomUser.objects.get(pk = request.user.id)
    rest = Restaurant_manager.objects.get(user_fk=user)

    all_bookings = Booking.objects.filter(restaurant_fk=rest.restaurant_fk,booking_type='none',date__gte=cdate).order_by('date')
    past_all_bookings = Booking.objects.filter(restaurant_fk=rest.restaurant_fk,booking_type='none',date__lt=cdate)
    all_booking_details = booking_details.objects.filter(booking_fk__in=all_bookings)
    past_booking_details = booking_details.objects.filter(booking_fk__in=past_all_bookings,date__lt=cdate)
    context = {
        'all_bookings':all_bookings,
        'all_booking_details':all_booking_details,
        'past':past_all_bookings,
        'past_booking_details':past_booking_details
    }
    return render(request,'manager_app/bookings.html',context)

def delete_booking(request,bookingid):
    bkid = Booking.objects.get(id=bookingid)
    tbls = booking_details.objects.filter(booking_fk=bkid)
    
    #using this loop we must have to make that particular tale status false so that other person can book that table
    for i in tbls:
        obj = booking_details.objects.get(id=i.id)
        table = Table.objects.get(id = obj.table_fk.id)
        table.status = 'False'
        table.save()

    if bkid.delete():
        return redirect('manager_app:bookings')
        
    context={

    }
    return render(request,'manager_app/bookings.html',context)

def del_food_item(request,pro_id):
    pro = Product.objects.get(pk=pro_id)
    pro.delete()
    return redirect('manager_app:food_items')

download_path = os.path.join(settings.MEDIA_ROOT,'invoice.pdf')
def top5_customer(request,id):
    rest = Restaurant.objects.get(pk=id)
    today = datetime.now()
    
    top_five_customers = Booking.objects.filter(restaurant_fk=rest).values('user_id__username','user_id__email').annotate(booking_count=Count('user_id__username')).order_by('-booking_count',)[:5]
    msg = 'Top 5 Customers based on bookings '

    context={
                'top_5':top_five_customers,
                'date':today,
                'msg':msg,
                'rest':rest,
                
    
    }    

    
    return pdf(context,'manager_app/all_bookings_reports.html')

def top5_foods(request,id):
    rest = Restaurant.objects.get(pk=id)
    today = datetime.now()
    top_five_food = Order_details.objects.filter(product_fk__restaurant_fk=rest).values('product_fk__product_name','product_fk__price').annotate(food_count=Count('product_fk__product_name')).order_by('-food_count',)[:5]
    
    context={
                'top_5':top_five_food,
                'date':today,
                'msg':'Top 5 foods based on bookings for this month',
                'rest':rest,
                
            }
    return pdf(context,'manager_app/top5_food_report.html')

def top3_decorations(request,id):
    rest = Restaurant.objects.get(pk=id)
    today = datetime.now()

    top3_decorations = Booking.objects.filter(restaurant_fk=rest).values('decoration_fk__decoration_type','decoration_fk__deco_price').annotate(decoration_count=Count('decoration_fk')).order_by('-decoration_count',)[:3]
    context={
                'top_3':top3_decorations,
                'date':today,
                'msg':'Top 3 Decorations Based on bookings',
                'rest':rest,
                
            }
    return pdf(context,'manager_app/top3_decorations.html')

def top3_restaurants(request,id):
    rest = Restaurant.objects.get(pk=id)
    today = datetime.now()

    top3_restaurants = Booking.objects.all().values('restaurant_fk__restaurant_name','restaurant_fk__address_fk__branch').annotate(rest_count=Count('restaurant_fk')).order_by('-rest_count',)[:3]
    context={
                'top_3':top3_restaurants,
                'date':today,
                'msg':'Top 3 Restaurants Based on bookings',
                'rest':rest,
                
            }
    return pdf(context,'manager_app/top3_restaurants.html')