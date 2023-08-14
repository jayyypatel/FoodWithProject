from django.urls import path
from . import views
# from .views import Generatepdf

app_name = 'customer_app'
urlpatterns = [
    path('',views.cust_profile,name='cust_profile'),
    path('<int:bookingid>/delete_booking/',views.delete_booking,name='delete_booking'),
    path('<int:bookingid>/delete_bookwidfood/',views.delete_bookwidfood,name='delete_bookwid_food'),
    path('<int:bid>/order_details/',views.order_details,name='order_details'),
    # path('payment/',views.payment,name='payment'),
    # path('pdf/', views.Generatepdf.as_view()),

]
