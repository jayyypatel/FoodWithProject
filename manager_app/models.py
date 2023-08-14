from django.db import models
from Auth_system.models import CustomUser
from restaurant.models import Restaurant


# Create your models here.
class Restaurant_manager(models.Model):
    user_fk = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='manager_usertbl',blank=True,null=True)
    restaurant_fk = models.OneToOneField(Restaurant,on_delete=models.CASCADE,related_name='manager_rest',blank=True,null=True)
    document = models.FileField(upload_to=None,blank=True,null=True)

    def __str__(self):
        return f'Manager: {self.user_fk}  Restaurant:- {self.restaurant_fk}' 
