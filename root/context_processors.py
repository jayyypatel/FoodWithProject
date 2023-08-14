from restaurant.models import Category, Order, Product, Restaurant
from Auth_system.models import CustomUser
def top_restaurants(request):
    restaurants = Restaurant.objects.all()[:6]
    cnt = Restaurant.objects.all().count()
    category = Category.objects.all()
    served = Order.objects.all().count
    users = CustomUser.objects.all().count
    t_foods= Product.objects.all().count
    return {'rest_context':restaurants,'cnt':cnt,'category':category,'served':served,
            'users_cnt':users,'food_cnt':t_foods
    }

