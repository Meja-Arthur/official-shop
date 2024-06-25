from django.shortcuts import render
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST




def add_to_cart(request, book_slug):
    cart = Cart(request)
    cart.add(book_slug)
    cart_length = len(cart)
    return JsonResponse({'cart_count': cart_length})


@require_POST
def remove_from_cart(request, book_slug):
    cart = Cart(request)
    cart.remove(book_slug)
    cart_length = len(cart)
    return JsonResponse({'cart_count': cart_length})
    

def cartpage(request):
    return render(request, 'cart/shop-cart.html',)


def checkoutpage(request):
    return render(request, 'cart/checkout-details.html', )

def paymentpage(request):
    return render(request, 'cart/checkout-payment.html',)

def review(request):
    return render(request, 'cart/checkout-review.html')