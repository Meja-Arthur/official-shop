from django.shortcuts import render
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt










def checkoutpage(request):
    return render(request, 'cart/checkout-details.html', )

def add_to_cart(request, book_slug):
    cart = Cart(request)
    cart.add(book_slug)
    return render(request, 'cart/menu_cart.html')

def cartpage(request):
 
    context = {
   
    }
    return render(request, 'cart/shop-cart.html', context)

def paymentpage(request):
    
    return render(request, 'cart/checkout-payment.html',)

def review(request):
    return render(request, 'cart/checkout-review.html')