from django.contrib import admin
from .models import Address, Booking, Category, Decoration,Book_with_order, Decoration_category, Order, Order_details , Rating , Restaurant , Product, Table ,booking_details, tables_time
# Register your models here.



admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Decoration_category)
admin.site.register(Decoration)
admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(Order_details)
admin.site.register(booking_details)
admin.site.register(Book_with_order)
admin.site.register(tables_time)