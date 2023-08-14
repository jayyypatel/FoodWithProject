from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart',views.index,name='cart'),
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('update/<int:product_id>/', views.basket_update, name='basket_update'),
]
