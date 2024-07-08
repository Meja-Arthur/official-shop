
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.contrib import messages
from django.conf import settings

from django.views import View
from .models import Book, BooksCategory, Author
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView

from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Book
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
import logging

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            
            return redirect(to='/')
        return render(request, self.template_name, {'form': form})
       
class CustomLoginView(LoginView):   
    form_class = LoginForm
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        
        return super(CustomLoginView, self).form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account-password-recovery.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('/')

def home(request):
    trending_books = Book.get_trending_books()
    recommended_books = Book.get_recommended_books()
    must_read = Book.get_must_read_books()
    
    context = {
        
        'trending_books': trending_books,
        'recommended_books': recommended_books,
        'must_read': must_read,   
    }
    return render(request, 'home.html', context)

def shop(request):
    
    categories = BooksCategory.objects.all() 
    books = Book.objects.all()
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(f"Total books: {len(books)}")
    print(f"Page number: {page_number}")
    print(f"Page object: {page_obj}")
    
 

    context = {

        'page_obj': page_obj,
        'categories': categories,
        
    }
    return render(request, 'shopbook.html', context)
    
def categorydetails(request, category_id):
    category = get_object_or_404(BooksCategory, id=category_id)
    books = Book.objects.filter(category=category)
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

  
    context = {
        'page_obj': page_obj,
    }
    return render(request,'category.html', context)   

@login_required
def bookdetails(request, slug):
    try:
        book = get_object_or_404(Book, slug=slug)
        host = request.get_host()
        price = f"{book.price:.2f}"  # Format the price to two decimal places
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': price,
            'item_name': book.title,
            'invoice':str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}/payment-success/{book.slug}/",
            'cancel_url': f"http://{host}/payment-failed/{book.slug}/",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        context = {
            'book': book,
            'paypal': paypal_payment
        }

        return render(request, 'shop-single.html', context)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in product_detail view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")


def PaymentSuccessful(request, slug):
    book = Book.objects.get(slug=slug)
    trending_books = Book.get_trending_books()[:4]  # Limit to 4 books
    context = {
        'book': book,
        'trending_books': trending_books
    }
    return render(request, 'payment-success.html', context)


def paymentFailed(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, 'payment-failed.html', {'book': book})
    
    
def download_book(request, slug):
    try:
        book = get_object_or_404(Book, slug=slug)
        file_path = book.file.path

        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return response
        else:
            raise Http404("Book not found")

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in download_book view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")
 
 
@login_required
def profile(request):
    return render(request, 'account-profile.html')
   
 
 
 
 
 
 
def add_to_wishlist(request, slug):
    pass
def wishlist(request):
    pass






def passwordforget(request):
    template = loader.get_template('account-password-recovery.html')
    return HttpResponse(template.render())
        
def address(request):
    template = loader.get_template('account-address.html')
    return HttpResponse(template.render())

def orders(request):
    template = loader.get_template('account-orders.html')
    return HttpResponse(template.render())

def profile(request):
    template = loader.get_template('account-profile.html')
    return HttpResponse(template.render())
    
def payment(request):
    template = loader.get_template('account-payment.html')
    return HttpResponse(template.render())

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template('contacts.html')
    return HttpResponse(template.render())
    
            
def sections(request):
    template = loader.get_template('shop-categories.html')
    return HttpResponse(template.render())            