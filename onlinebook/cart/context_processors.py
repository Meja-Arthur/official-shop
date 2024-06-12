from .cart import Cart

def cart(request):
    try:
        cart = Cart(request)
        print(f"Cart initialized successfully. Cart length: {len(cart)}")  # Debugging statement
        return {'cart': cart}
    except Exception as e:
        print(f"Error initializing cart: {e}")  # Debugging statement
        return {'cart': None}