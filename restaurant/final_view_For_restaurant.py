
from decimal import Decimal
from time import  timezone
from django.shortcuts import render, redirect
from Auth_system.models import CustomUser
from django.http import HttpResponseRedirect
from cart.basket import Basket
from restaurant.forms import book_detail_Form, booking_Form, tbl_Form
from .models import Booking, Category, Decoration_category, Order, Order_details, Product, Restaurant, Table, booking_details, Book_with_order, tables_time
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cart.forms import AddQuantityForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
import razorpay
from django.conf import settings
#for email
from django.core.mail import send_mail
from datetime import timedelta,datetime,time
# this return restaurant page on webpage


def index(request):
    restaurant = Restaurant.objects.all()
    context = {
        'rest_name': restaurant
    }
    # restaurants.html
    return render(request, 'restaurant/restaurants.html', context)


def cat_restaurants(request, cat_id):
    cat_obj = Category.objects.get(pk=cat_id)
    cat_wise_restaurant = Restaurant.objects.filter(category_fk=cat_obj)
    context = {
        'rest_name': cat_wise_restaurant
    }
    return render(request, 'restaurant/restaurants.html', context)

# this return resaurant_details page on webpage
@login_required(login_url='Auth_system:login_user_n')
def restaurant_details(request, rest_id):

    products_by_rest = Product.objects.filter(restaurant_fk=rest_id)

    # !     for book table operations
    l_user = CustomUser.objects.get(pk=request.user.id)
    # ,status=False  to find only false tables means available tbls
    available_tbl = Table.objects.filter(restaurant_fk=rest_id)
    deco_type = Decoration_category.objects.all()

    form = booking_Form()
    bdetails_form = book_detail_Form()
    tbl_form = tbl_Form()
    # ? request.POST.getlist('services')
    cart_product_form = AddQuantityForm()

    if request.method == 'POST':
        form = booking_Form(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = l_user  # logged in user
            select_deco = request.POST['decoration_select']
            selected_hour = request.POST['hour_select']
            # * this queryset will return record by only first word of select_decoration using split function
            deco = Decoration_category.objects.get(
                decoration_type=select_deco.split()[0])
            form.decoration_fk = deco
            rest_id = Restaurant.objects.get(id=rest_id)
            form.restaurant_fk = rest_id
            
            tbl_booked = request.POST.getlist('tbl_booked')
            tot = 0
            for j in tbl_booked:
                tot += form.decoration_fk.deco_price
            form.total_price = tot
            form.booking_type = 'none'
            #for user select hours
            if int(selected_hour) < 1:
                selected_hour = 1
            form.reserved_table = selected_hour 
            
            time_Str = timedelta(hours=form.time.hour,minutes=form.time.minute,seconds=form.time.second)+timedelta(hours=int(form.reserved_table))
            start_str = timedelta(hours=form.time.hour,minutes=form.time.minute,seconds=form.time.second)
            start_time = datetime.strptime(str(start_str),"%H:%M:%S")
            book_til = datetime.strptime(str(time_Str),"%H:%M:%S")
            form.book_til = book_til

            
            
            #! aleady booked functionality
            tbl_booked = request.POST.getlist('tbl_booked')
            for i in tbl_booked:
                tbl = Table.objects.get(tbl_name=i)
                
                for i in  tables_time.objects.filter(date=form.date, tbl_fk=tbl):
                    
                    
                    
                    #todo it is used to check time gaps and if book_til time is between book.time and book.book_til give than error
                    if start_time > datetime.strptime(str(i.time),"%H:%M:%S") and start_time < datetime.strptime(str(i.book_til),"%H:%M:%S"):
                        
                        messages.warning(
                            request, f'{tbl.tbl_name} is all ready booked at a time please choose other Table')
                        return redirect('restaurant:restaurant_details', rest_id.id)
                    #todo it is used to check booktil time 
                    if book_til > datetime.strptime(str(i.time),"%H:%M:%S") and book_til < datetime.strptime(str(i.book_til),"%H:%M:%S"):
                        
                        messages.warning(
                            request, f'{tbl.tbl_name} is all ready booked at a time please choose other Table')
                        return redirect('restaurant:restaurant_details', rest_id.id)

            form.save()

            # ? its return latest object by id used meta class in models
            bid = Booking.objects.latest()

            #! getlist is used to get multiple selected items in requests
            tbl_booked = request.POST.getlist('tbl_booked')
            bdetails_form = bdetails_form.save(commit=False)
            # tbl_form = tbl_form.save(commit=False)
            # this loop store multiple record at time if user select multiple record
            # if user select one tbl than loop will go only one time simple
            for i in tbl_booked:

                tbl = Table.objects.get(tbl_name=i)
                bdetail_table = booking_details.objects.create(
                    booking_fk=bid, table_fk=tbl, date=bid.date, time=bid.time,booking_type='none')
                bdetail_table.save()
                tables_time.objects.create(tbl_fk=tbl,date=bid.date,time=bid.time,book_til=book_til)
                # bdetails_form.booking_fk = bid
                # tbl = Table.objects.get(tbl_name = i)
                # bdetails_form.table_fk = tbl
                # bdetails_form.save()

                # ? this will update record particularly and then save() in Table
                tbl.status = 'True'
                tbl.date = bid.date
                tbl.time = bid.time
                tbl.save()
                # print(i)

            #to make total amount and send to razorpay api 
            amount = bid.total_price*100
            if amount <=0:
                amount=1*100
            client = razorpay.Client(auth=("rzp_test_susforIvG6nYky", "VUQ8dfvBSkVS9Lstz9r1pQ9r"))
            payment = client.order.create({'amount':amount , 'currency': 'INR','payment_capture': '1'})

            bid.razorpay_order_id = payment['id']
            bid.save()

            return render(request, 'restaurant/razorpay.html', {'payment': payment})
        

    context = {
        'restaurant': Restaurant.objects.get(id=rest_id),
        'products': products_by_rest,
        'b_form': form,
        'deco_type': deco_type,
        'available_tbl': available_tbl,
        'cart_product_form': cart_product_form
    }
    # restaurant_details.html
    return render(request, 'restaurant/restaurant_details.html', context)

# this return menu page on webpage


def menu(request):
    return render(request, 'restaurant/menu.html')

# it return services page on webpage


def services(request):
    return render(request, 'restaurant/services.html')


def myorder(request):
    return render(request, 'restaurant/mybookings.html')


#! book tbl withorder
def book_tbl_withorder(request):

    # ? to access basket details
    basket = Basket(request)
    # *print(basket.basket) output of print {'1': {'price': '500.00', 'qty': 7}, '3': {'price': '656.00', 'qty': 5}}

    if bool(basket):  # this will check basket/distionary is empty
        cart_product_id = list(basket.basket.keys())[0]
        cart_restaurant_id = get_object_or_404(
            Product, id=cart_product_id).restaurant_fk.id
    else:
        return redirect('cart:cart')

    available_tbl = Table.objects.filter(
        restaurant_fk=cart_restaurant_id)  # ,status=False
    l_user = CustomUser.objects.get(pk=request.user.id)
    deco_type = Decoration_category.objects.all()
    form = booking_Form()
    bdetails_form = book_detail_Form()

    if request.method == 'POST':
        form = booking_Form(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = l_user  # logged in user
            select_deco = request.POST['decoration_select']
            selected_hour = request.POST['hour_select']
            
            # * this queryset will return record by only first word of select_decoration using split function
            deco = Decoration_category.objects.get(
                decoration_type=select_deco.split()[0])
            form.decoration_fk = deco
            rest_id = Restaurant.objects.get(id=cart_restaurant_id)
            form.restaurant_fk = rest_id
            
            tbl_booked = request.POST.getlist('tbl_booked')
            tot = 0
            for j in tbl_booked:
                tot += form.decoration_fk.deco_price
            form.total_price = tot
            form.booking_type = 'dine-in'
            form.b_type='dine-in'
            #for user select hours
            if int(selected_hour) < 1:
                selected_hour = 1
            form.reserved_table = selected_hour

            #this will add hour in database
            time_Str = timedelta(hours=form.time.hour,minutes=form.time.minute,seconds=form.time.second)+timedelta(hours=int(form.reserved_table))
            start_str = timedelta(hours=form.time.hour,minutes=form.time.minute,seconds=form.time.second)
            start_time = datetime.strptime(str(start_str),"%H:%M:%S")
            book_til = datetime.strptime(str(time_Str),"%H:%M:%S")
            form.book_til = book_til

            #! aleady booked functionality
            tbl_booked = request.POST.getlist('tbl_booked')
            for i in tbl_booked:
                tbl = Table.objects.get(tbl_name=i)
                
                for i in  tables_time.objects.filter(date=form.date, tbl_fk=tbl):
                    
                    
                    
                    #todo it is used to check time gaps and if book_til time is between book.time and book.book_til give than error
                    if start_time > datetime.strptime(str(i.time),"%H:%M:%S") and start_time < datetime.strptime(str(i.book_til),"%H:%M:%S"):
                        
                        messages.warning(
                            request, f'{tbl.tbl_name} is all ready booked at a time please choose other Table')
                        return redirect('cart:cart')
                    #todo it is used to check booktil time 
                    if book_til > datetime.strptime(str(i.time),"%H:%M:%S") and book_til < datetime.strptime(str(i.book_til),"%H:%M:%S"):
                        
                        messages.warning(
                            request, f'{tbl.tbl_name} is all ready booked at a time please choose other Table')
                        return redirect('cart:cart')

            form.save()

            # ? its return latest object by id used meta class in models
            bid = Booking.objects.latest()

            #! getlist is used to get multiple selected items in requests
            tbl_booked = request.POST.getlist('tbl_booked')
            bdetails_form = bdetails_form.save(commit=False)
            # tbl_form = tbl_form.save(commit=False)
            # this loop store multiple record at time if user select multiple record
            # if user select one tbl than loop will go only one time simple
            for i in tbl_booked:

                tbl = Table.objects.get(tbl_name=i)
                bdetail_table = booking_details.objects.create(
                    booking_fk=bid, table_fk=tbl, date=bid.date, time=bid.time,booking_type='dine-in')
                tables_time.objects.create(tbl_fk=tbl,date=bid.date,time=bid.time,book_til=book_til)
                bdetail_table.save()
                # bdetails_form.booking_fk = bid
                # tbl = Table.objects.get(tbl_name = i)
                # bdetails_form.table_fk = tbl
                # bdetails_form.save()

                # ? this will update record particularly and then save() in Table
                tbl.status = 'True'
                tbl.date = bid.date
                tbl.time = bid.time
                tbl.save()
                # print(i)

            # this will used to first make order object after order details object

            place_order = Order.objects.create(
                user_id=l_user, order_date=bid.date, order_type='dine-in')
            print(place_order)

            total = 0
            # *print(basket.basket) output of print {'1': {'price': '500.00', 'qty': 7}, '3': {'price': '656.00', 'qty': 5}}
            # *this for loop makes Order_details records/objects upto total keys that means total products in basket/cart
            for i in basket.basket.keys():
                pro_obj = Product.objects.get(id=i)
                detail_total = Decimal(
                    basket.basket[i]['price']) * Decimal(basket.basket[i]['qty'])
                order_details = Order_details.objects.create(
                    order_fk=place_order, product_fk=pro_obj, quantity=basket.basket[i]['qty'], total_amount=detail_total)
                total += detail_total
                print('yoyoyoyoyoyoyoyoyoyoyoyyo')

            place_order.final_price = total
            place_order.save()

            # * here we are creating 'Book_with_order' object for order with booking
            # this total is mix of booking id total and place order totol
            bwo_total = place_order.final_price + bid.total_price
            Bookworder_obj = Book_with_order.objects.create(
                booking_id=bid, order_id=place_order, total=bwo_total)
            print(Bookworder_obj)

            # * now we have to remove all cart objects in basket

            for i in list(basket.basket.keys()):
                print(i)
                pro_obj = Product.objects.get(id=i)
                # its a basket class method delete to del product one by one
                basket.delete(pro_obj)
            print('its all free')

            #to make total amount and send to razorpay api 
            amount= int(total + bid.total_price)*100 
            
            client = razorpay.Client(auth=("rzp_test_susforIvG6nYky", "VUQ8dfvBSkVS9Lstz9r1pQ9r"))
            payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})

            bid.razorpay_order_id = payment['id']
            bid.save()
            return render(request, 'restaurant/razorpay.html', {'payment': payment})

    context = {
        'rest': get_object_or_404(Product, id=cart_product_id).restaurant_fk,
        'deco_type': deco_type,
        'b_form': form,
        'available_tbl': available_tbl,
    }
    return render(request, 'restaurant/book_tbl_withorder.html', context)

def food_details(request, proid):
    pro = Product.objects.get(id=proid)
    cart_product_form = AddQuantityForm()
    context = {
        'product': pro,
        'cart_product_form': cart_product_form
    }
    return render(request, 'restaurant/food_details.html', context)


def search_restaurant(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if not query:
            return redirect('root:index')
        else:

            lookups = Q(restaurant_name__icontains=query) | Q(
                category_fk__type__icontains=query)

            results = Restaurant.objects.filter(lookups).distinct()

            if results.exists():

                context = {'results': results,

                           'r_count': results.count()
                           }
                return render(request, 'restaurant/search_resto.html', context)
            else:

                return render(request, 'restaurant/searchnotfound.html', {'query': query})

    else:
        return render(request, 'restaurant/search_resto.html')

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        book = Booking.objects.filter(razorpay_order_id = order_id).first()
        book.paid = True
        book.save()

        l_user = CustomUser.objects.get(pk=request.user.id)
        subject = 'Order placed..'
        message = f'Your order has been placed and Razorpay payment id is : {order_id}'
        to_mail = l_user.email



        send_mail(
                subject, #'Subject here',
                message, #'Here is the message.',
                settings.EMAIL_HOST_USER, #'from@example.com',

                [to_mail ],
                 fail_silently=False,
        )
        # msg_plain=render_to_string('email.txt')
        # msg_html=render_to_string('email.html')

        # send_mail("Your donation has been received",msg_plain,settings.EMAIL_HOST_USER,
        #             ["rajlogicrays@gmail.com"],# [user.email],
        #             html_message=msg_html)

    return render(request, "restaurant/success.html")