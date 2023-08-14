from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class registerUser(UserCreationForm):

    class Meta:
        model = CustomUser  #database 
        fields = ('username','email','password1', 'password2','user_choice')
        widgets = {
                'user_choice':forms.RadioSelect(attrs={'class':"form-check-flex list-unstyled ",'type':'radio','style':'height:10px'})
        }
    
class loginUser(AuthenticationForm):
    pass