from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import RegisterView, CustomLoginView, ResetPasswordView
from .forms import LoginForm

from django.contrib.auth.forms import PasswordResetForm
from cart.views import add_to_cart, cartpage, checkoutpage, paymentpage, review, remove_from_cart

from django.contrib.auth import views as auth_views


app_name = 'book'
urlpatterns = [
    
    path('', views.home, name='home'),
    path('shop/', views.shop,  name='shop'),
    path('book/<slug:slug>/', views.bookdetails, name='book-details'),
    path('download_book/<slug:slug>/', views.download_book, name='download_book'),
    path('payment-success/<slug:slug>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<slug:slug>/', views.paymentFailed, name='payment-failed'),
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    path('section/', views.sections, name='sections'),#delt with later in future events 
    
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html',
                                           authentication_form=LoginForm), name='login'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    
    
    path('category/<int:category_id>/', views.categorydetails, name='category'),
    
    
    path('cart/', cartpage, name='cart'),
    path('add_to_cart/<slug:book_slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:book_slug>/', remove_from_cart, name='remove_from_cart'),
    
    
    
    path('checkout/', checkoutpage, name='checkout'),
    
   
    
    path('payment/', paymentpage, name='payment'),
    path('review/', review, name='review'),
  
   
    path('password/', views.passwordforget, name='password'),
    path('address/', views.address, name='address'),
    path('order/', views.orders, name='orders'),
    
    path('payment/', views.payment, name='payment'),
   
    
    
   

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
    
]
