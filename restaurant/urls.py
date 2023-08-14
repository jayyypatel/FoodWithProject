from django.urls import path
from . import views
app_name = 'restaurant'

urlpatterns = [
    path('indexrestaurant/',views.index,name='indexrestaurant'),
    path('<int:rest_id>/restaurant_details/',views.restaurant_details,name='restaurant_details'),
    path('menu/',views.menu,name='menu'),
    path('services/',views.services,name='services'),
    path("mybookings/", views.myorder, name="mybookings"),
    path("<int:proid>/food_details/", views.food_details, name="food_details"),
    path("book_tbl_withorder/", views.book_tbl_withorder, name="book_tbl_withorder"),
    path("search_restaurant/", views.search_restaurant, name="search_restaurant"),
    path('<int:cat_id>/cat_restaurants',views.cat_restaurants,name='cat_restaurants'),
    path('success/' , views.success , name='success'),
]