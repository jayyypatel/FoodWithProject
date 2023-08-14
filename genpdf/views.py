from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings
import os
from restaurant.models import Booking,Book_with_order, Order_details,booking_details
os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")



def pdf_order_details(request):
    b = Booking.objects.get(pk=171)
    details = booking_details.objects.filter(booking_fk=b)

    context = {
        'details' : details
    }
    return render(request, 'genpdf/invoice.html', context=context)

download_path = os.path.join(settings.MEDIA_ROOT,'invoice.pdf')


def download_orders(request,id):
    b = Booking.objects.get(pk=id)
    tbl_b_Details = booking_details.objects.filter(booking_fk=b)
    bworder_obj = Book_with_order.objects.get(booking_id=b)
    order_details = Order_details.objects.filter(order_fk=bworder_obj.order_id)
    orderdetails_total = 0
    for i in order_details:
        orderdetails_total += i.quantity * i.product_fk.price
    final_total = orderdetails_total + b.total_price

    context = {
        'order_details':order_details,
        'bworder_obj':bworder_obj,
        'orderdetails_total':orderdetails_total,
        'final_total':final_total,
        'tbl_b_Details':tbl_b_Details,
        'b':b,
        
    }    

    template_render  = render_to_string('genpdf/invoice.html', context)
    html = HTML(string=template_render)
    html.write_pdf(target=download_path)

    fs = FileSystemStorage(settings.MEDIA_ROOT)
    with fs.open('invoice.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response
    return response