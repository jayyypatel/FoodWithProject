from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from restaurant.models import Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .basket import Basket
from .forms import AddQuantityForm


def index(request):
    basket = Basket(request)
    for item in basket:
        item['update_quantity'] = AddQuantityForm(initial= {'quantity' : item['qty']})
    cart_restaurant_id =0
    if bool(basket):  # this will check basket/distionary is empty or note
        cart_product_id = list(basket.basket.keys())[0]
        cart_restaurant_id = get_object_or_404(
            Product, id=cart_product_id).restaurant_fk.id
    
    context ={
        'cart' : basket,
        'flag': cart_restaurant_id
    }
    return render(request,'cart/cart.html',context)

@login_required(login_url='Auth_system:login_user_n')
@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    if basket.basket:
        cart_product_id = list(basket.basket.keys())[0]
        cart_product_restaurant = get_object_or_404(Product, id=cart_product_id).restaurant_fk
        product_restaurant = get_object_or_404(Product, id=product_id).restaurant_fk
        if cart_product_restaurant == product_restaurant:
            product = get_object_or_404(Product, id=product_id)
            print(product.restaurant_fk)
            form = AddQuantityForm(request.POST)
    
            if form.is_valid():
                cd = form.cleaned_data
                basket.add(product=product, qty=cd['quantity'])
                
            return redirect('cart:cart') 
        else:
            
            messages.warning(request, 'You have to select same restaurant Food')
            return redirect('cart:cart') 
    else:
        basket = Basket(request)
    # print(basket.basket)
        product = get_object_or_404(Product, id=product_id)
        form = AddQuantityForm(request.POST)
    
        if form.is_valid():
            cd = form.cleaned_data
            basket.add(product=product, qty=cd['quantity'])
        # print(basket.basket)
        return redirect('cart:cart') 

@require_POST        
def basket_remove(request, product_id):
    basket = Basket(request)
    print(basket.basket)
    product = get_object_or_404(Product, id=product_id)
    basket.delete(product)
    print(basket.basket)
    return redirect('cart:cart') 

@require_POST
def basket_update(request, product_id):
    basket = Basket(request)
    print(basket.basket)
    product = get_object_or_404(Product, id=product_id)
    form = AddQuantityForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        qty = cd['quantity']
        basket.update(product=product, qty=qty)
        print(basket.basket)
    return redirect('cart:cart')     
        
