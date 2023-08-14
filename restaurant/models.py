from datetime import datetime,time
from itertools import product
from os import truncate
from pickle import TRUE
from turtle import mode
from django.utils import timezone
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.indexes import Index
from Auth_system.models import CustomUser
import datetime
from django.core.validators import MinValueValidator
# Create your models here.



class Address(models.Model):
    branch = models.CharField(max_length=30)
    street_address = models.CharField(max_length=70)
    city = models.CharField(max_length=35)
    pincode = models.IntegerField()
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.branch



class Category(models.Model):
    type = models.CharField(max_length=20)

    def  __str__(self):
        return f"{self.type}"

class Rating(models.Model):
    score = models.DecimalField(max_digits=7,decimal_places=2)
    feedback = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.score}' 


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    contact_no = models.CharField(max_length=10)
    address_fk = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='rest_address')
    category_fk = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='rest_category')
    opening_hours = models.CharField(max_length=15)
    takeaway = models.BooleanField()
    rating_fk = models.ForeignKey(Rating,on_delete=models.CASCADE,related_name='rest_rating')
    picture = models.ImageField(upload_to='images',blank=True,null=True)
    minimum_or = models.IntegerField(blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.restaurant_name

class Product(models.Model):     
                       
    product_name =  models.CharField(max_length=30,db_index=True)
    price =  models.DecimalField(max_digits=8,decimal_places=2)
    category_fk = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product_category')
    description  = models.CharField(max_length=83)
    product_img = models.ImageField(upload_to='images',blank=True,null=True)
    restaurant_fk = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='rest_product')
    discount = models.IntegerField()
    available = models.BooleanField(default=True,null=True,blank=True)
    def __str__(self):
        return f'{self.product_name}  ||  Rest - {self.restaurant_fk}' 

#options for decoration category
ops = (
    ('none','None'),
    ('birthday','Birthday'),
    ('anniversary','Anniversary'),
    ('wedding','Wedding'),
    ('party','Party'),
    ('Candle-light','Candle-light')
)
class Decoration_category(models.Model):
    decoration_type = models.CharField(max_length=20,choices=ops,default='none')
    deco_price = models.IntegerField()
    
    def __str__(self):
        return f'Type: {self.decoration_type} '

#decoration table 
class Decoration(models.Model):
    decoration_cat_fk = models.ForeignKey(Decoration_category,on_delete=models.CASCADE,related_name='deco_deco_category')
    restaurant_fk = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='deco_restaurant')

#for tables management
# class Table(models.Model):
#     numberof_tables = models.IntegerField(blank=True,null=True)           #10   total tables in restaurant
#     available_table_status = models.IntegerField(blank=True,null=True)     #10
#     booked_tbl = models.IntegerField(blank=True,null=True)                  #0                                                                    #0
#     restaurant_fk = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='table_rest')


#for real time table booking with tables newwwwwwwwwwwww modellllllllllllllllllllllllllllllllll
class Table(models.Model):          
    status = models.BooleanField(default=False)    
    date = models.DateField(default=timezone.now,blank=True,null=True)
    time = models.TimeField(default=timezone.now,blank=True,null=True)
    tbl_name = models.CharField(max_length=10,blank=True,null=True,unique=True)
    restaurant_fk = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='table_rest')
    max = models.CharField(max_length=10,blank=True,null=True,default=4)

    def __str__(self):
        return f'{self.tbl_name} R:- {self.restaurant_fk}'

ord_type = (
    ('takeaway','Takeaway'),
    ('dine-in','dine-in'),
    ('none','None')
)
# todo: this is master table for booking_details tbl
#booking table for storing bookings
class Booking(models.Model):
    name = models.CharField(max_length=20,blank=True,null=True)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='booking_usertbl')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    book_til = models.TimeField(default=timezone.now,blank=True,null=True)
    num_of_person = models.CharField(max_length=3)
    reserved_table = models.CharField(max_length=3,blank=True,null=True)     #store booking hours
    decoration_fk = models.ForeignKey(Decoration_category,on_delete=models.CASCADE,related_name='booking_decocat')
    total_price = models.IntegerField(blank=True,null=True)
    restaurant_fk = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='booking_rest')
    #used to time filter
    booking_type = models.CharField(max_length=10,choices=ord_type,default='none',blank=True)
    b_type = models.CharField(max_length=10,choices=ord_type,default='none',blank=True)
    #for razorpay use
    razorpay_order_id = models.CharField(max_length=1000,blank=True,null=True)
    paid = models.BooleanField(default=False,blank=True,null=True)
    confirm = models.BooleanField(default=False,blank=True,null=True)

    class Meta:
        get_latest_by = 'pk'

class booking_details(models.Model):
    booking_fk = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='bdetails_booking')
    table_fk = models.ForeignKey(Table,on_delete=models.CASCADE,related_name='bdetails_table')
    date = models.DateField(default=timezone.now,blank=True,null=True)
    time = models.TimeField(default=timezone.now,blank=True,null=True)
    booking_type = models.CharField(max_length=10,choices=ord_type,default='none',blank=True)

class tables_time(models.Model):
    tbl_fk= models.ForeignKey(Table,on_delete=models.CASCADE,related_name='time_table')
    date = models.DateField(default=timezone.now,blank=True,null=True)
    time = models.TimeField(default=timezone.now,blank=True,null=True)
    book_til = models.TimeField(default=timezone.now,blank=True,null=True)
    

#order table
ord_status = (
    ('confirmed','Confirmed'),
    ('canceled','Canceled'),
    ('done','Done')
)


class Order(models.Model):
    
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order_usertbl')
    final_price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    order_date = models.DateField(default=timezone.now)
    order_status = models.CharField(max_length=10,choices=ord_status,default='confirmed')
    order_type = models.CharField(max_length=10,choices=ord_type,default='takeaway',blank=True)
    

#order details table to store particular order details
class Order_details(models.Model):
    order_fk = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_detail_order')
    product_fk = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_detail_product')
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=8,decimal_places=2)  # use functionality 

#this table is used to store table booking with that table order
class Book_with_order(models.Model):
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='bwo_booking')
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='bwo_order')
    total = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    

# class tbl_With_food(models.Model):  #food with table mix model 
#     user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='tbl_w_food_usertbl')
#     date = models.DateField(default=timezone.now)
#     time = models.TimeField(default=timezone.now)
#     num_of_person = models.CharField(max_length=3)
#     reserved_table = models.CharField(max_length=3)
#     decoration_fk = models.ForeignKey(Decoration,on_delete=models.CASCADE,related_name='tbl_w_food_deco')
#     total_price = models.IntegerField()
#     restaurant_fk = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='tbl_w_rest')

# class fwt_orders(models.Model):     #food with table orderdetails
#     fwt_fk = models.ForeignKey(tbl_With_food,on_delete=models.CASCADE,related_name='fwt_orders_tbl')
#     product_fk = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='fwt_orders_product')
#     quantity = models.IntegerField()
#     total_amount = models.DecimalField(max_digits=8,decimal_places=2)