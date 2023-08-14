from django.urls import path
from . import views


app_name = 'genpdf'

urlpatterns = [
    path("", views.pdf_order_details, name='order_details'),
    path('<int:id>/download_orders/', views.download_orders, name='download_invoice'),
]
