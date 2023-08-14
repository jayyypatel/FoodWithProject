from datetime import datetime
from ssl import Purpose
from urllib import response
from django.conf import settings
from xhtml2pdf import pisa
# from .utils import render_to_pdf
from django.views import View
from xhtml2pdf.pisa import pisaDocument
from django.template import RequestContext
from io import BytesIO, StringIO
# from customer_app.utils import render_to_pdf
from django.shortcuts import redirect
from django.shortcuts import render
from Auth_system.models import CustomUser
from django.http import HttpResponse

from restaurant.models import Book_with_order, Booking, Order, Order_details, Table, booking_details
from django.template.loader import get_template

# Create your views here.
def cust_profile(request):
    cdate = datetime.now()
    user = CustomUser.objects.get(pk=request.user.id)
    #used to get only tbl booking items
    tbl_bookings = Booking.objects.filter(user_id=user,booking_type='none',date__gt=cdate)
    b = booking_details.objects.all()
    
    #this is used to get food with booking
    fwt_booking = Booking.objects.filter(user_id=user,booking_type='dine-in',date__gt=cdate)[::-1]#b_type
    print(fwt_booking)
    
    obj = Booking.objects.filter(user_id=user,date__lt=cdate)
    print(obj)
    context = {
        'tbl_booking':tbl_bookings,
        'fwt_booking':fwt_booking,
        'user':user,
        'b':b,
        'less_date':obj
        
    }
    return render(request,'customer_app/cust_profile.html',context)

#only delete booking without food
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
        return redirect('customer_app:cust_profile')
        

    context = {

    }
    return render(request,'customer_app/cust_profile.html',context)

    
def delete_bookwidfood(request,bookingid):
    bkid = Booking.objects.get(id=bookingid)
    tbls = booking_details.objects.filter(booking_fk=bkid)
    
    #using this loop we must have to make that particular tale status false so that other person can book that table
    for i in tbls:
        obj = booking_details.objects.get(id=i.id)
        table = Table.objects.get(id = obj.table_fk.id)
        table.status = 'False'
        table.save()

    bworder_obj = Book_with_order.objects.get(booking_id=bkid)
    order_obj = Order.objects.get(pk=bworder_obj.order_id.id)
    bkid.delete()
    order_obj.delete()
    return render(request,'customer_app/cust_profile.html')

def order_details(request,bid):
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
    return render(request,'customer_app/order_details.html',context)



# def payment(request):
#     try:
#         response = api.payment_request_create(
#             amount = 300,
#             purpose = 'Order Process',
#             buyer_name = 'Jay Patel',
#             email = 'jayp15813@gmail.com',
#             redirect_url = 'http://127.0.0.1:8000/order-success/'
#         )
#         print(response)
#         context = {
#             'payment_url' : response['payment_request']['longurl']

#         }
#         return render(request,'restaurant/restaurant_details.html',context)
#     except Exception as e:
#         print(e)

# class Generatepdf(View):
#     def get(self,request):
#         pdf = render_to_pdf('customer_app/invoice.html',{'mylist':'helloooooooooo'})
#         return HttpResponse(pdf,content_type='application/pdf')
