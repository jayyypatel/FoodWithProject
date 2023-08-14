from django.urls import path
from . import views

app_name = 'manager_app'

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('orderlist/',views.orderlist,name='orderlist'),
    path('<int:id>/confirmation/',views.confirmation,name='Confirmation'),
    path('<int:bid>/pr_order_details/',views.pr_order_details,name='pr_order_details'),
    path('regi_rest/',views.register_rest,name='regi_rest'),
    path('product_regi/',views.register_pro,name='product_regi'),
    path('tbl_regi/',views.register_tbl,name='tbl_regi'),
    path('tbl_details/',views.tbl_details,name='tbl_details'),
    # path('bookings/',views.bookings,name='bookings'),
    path('food_items/',views.food_items,name='food_items'),
    path('upcomming_bookings/',views.upcomming_booking,name='upcomming_booking'),
    path('<int:bookingid>/delete_bookings/',views.delete_booking,name='delete_booking'),
    path('<int:pro_id>/del_food_items/',views.del_food_item,name='del_food_items'),
    path('<int:tbl_id>/del_tbl/',views.del_tbl,name='del_tbl'),
    path('<int:id>/top5_customer/',views.top5_customer,name='top5_customer'),
    path('<int:id>/top5_foods/',views.top5_foods,name='top5_foods'),
    path('<int:id>/top3_decorations/',views.top3_decorations,name='top3_decorations'),
    path('<int:id>/top3_restaurants/',views.top3_restaurants,name='top3_restaurants'),
]
