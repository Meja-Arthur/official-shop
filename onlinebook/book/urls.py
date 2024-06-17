from django.urls import path
from . import views
from django.contrib.auth import views as auth_view



from django.contrib.auth.forms import PasswordResetForm
from cart.views import add_to_cart, cartpage, checkoutpage, paymentpage, review




app_name = 'book'
urlpatterns = [
    
    path('', views.home, name='home'),
    path('shop/', views.shop,  name='shop'),
    path('book/<slug:slug>/', views.bookdetails, name='book-details'),
    
    
    path('cart/', cartpage, name='cart'),
    path('add_to_cart/<slug:book_slug>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkoutpage, name='checkout'),
    
    
    
    path('payment/', paymentpage, name='payment'),
    path('review/', review, name='review'),
    path('wishlist/', views.wishlist, name='wishlist'),
   
    path('password/', views.passwordforget, name='password'),
    path('address/', views.address, name='address'),
    path('order/', views.orders, name='orders'),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.payment, name='payment'),
   
    
    
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name="login"),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
    
]