from django.shortcuts import render
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt











def add_to_cart(request, book_slug):
    cart = Cart(request)
    cart.add(book_slug)
    cart_length = len(cart)
    return JsonResponse({'cart_count': cart_length})


def remove_from_cart(request, book_slug):
    print("Removing book with slug:", book_slug)  # Debugging
    try:
        cart = Cart(request)
        cart.remove(book_slug)
        cart_length = len(cart)
        cart_total = cart.get_total_cost()
        print("Cart length:", cart_length, "Cart total:", cart_total)  # Debugging
        return JsonResponse({
            'cart_count': cart_length,
            'cart_total': cart_total,
        })
    except Exception as e:
        print("Error removing book from cart:", e)  # Debugging
        return JsonResponse({
            'error': str(e)
        }, status=500)
        
        
        

def cartpage(request):
    return render(request, 'cart/shop-cart.html',)


def checkoutpage(request):
    return render(request, 'cart/checkout-details.html', )

def paymentpage(request):
    return render(request, 'cart/checkout-payment.html',)

def review(request):
    return render(request, 'cart/checkout-review.html')