from datetime import datetime
from logging import PlaceHolder
from pyexpat import model
from django.db.models import fields

from .models import Address, Booking, Category, Rating, Restaurant, Table, booking_details
from django import forms

class rest_registerForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['restaurant_name','email','contact_no','opening_hours','takeaway','picture','minimum_or','description' ]
        widgets ={
            
        }
    
class address_registerForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['branch','street_address','city','pincode','state']


class category_registerForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['type']
        Labels ={
            'type':'Restaurant Category'
        }
class rating_Form(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']


class tbl_Form(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['status','date','time','tbl_name']
        widgets = {
            'status' : forms.CheckboxInput(attrs={'class':'onoffswitch','id': 'myonoffswitch'}),
            'date' : forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'date','min':datetime.now().date}),
            'time' : forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'time'}),
            'tbl_name': forms.TextInput(attrs={'class': 'form-control datepicker-default form-control picker__input','placeholder':'helllo','type':'text','required':'True'})
        }

class booking_Form(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name','date','time','num_of_person']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}),
            'date': forms.NumberInput(attrs={'class':'form-control datepicker' ,'type':'date','placeholder':'Enter Date for Booking','min':datetime.now().date}),
            'time': forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'time','format':'%I:%M:%p','min':datetime.now()}),
            'num_of_person': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter How many person are coming'}),
            
        }

class book_detail_Form(forms.ModelForm):
    class Meta:
        model = booking_details
        fields = ['booking_fk','table_fk']