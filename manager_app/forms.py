from django import forms
from django.forms import fields
from restaurant.models import Product
from .models import Restaurant_manager

class manager_Form(forms.ModelForm):
    class Meta:
        model = Restaurant_manager
        fields = ['user_fk','restaurant_fk']

class product_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','price','category_fk','description','product_img','discount']