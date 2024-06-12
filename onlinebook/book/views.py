
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.contrib import messages
from django.conf import settings

from django.views import View
from .models import Book, BooksCategory, Customer, Author
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login,logout

from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Book

def registerUser(request): 
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for ' + user)
            return redirect('/login')
        
    context = {'form':form}
    return render(request, 'register.html', context)
    
def loginUser(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, "There was an error please check you credential and  try again.")
            return redirect('/login')
            
    else:
        return render(request, 'login.html')



def home(request):
    trending_books = Book.get_trending_books()
    recommended_books = Book.get_recommended_books()
    must_read = Book.get_must_read_books()
    
    #split must_read books into three parts 
    part_size = (len(must_read) + 2) // 3
    must_read_1 = must_read[:part_size]
    must_read_2 = must_read[part_size:part_size*2]
    must_read_3 = must_read[part_size*2:]
    
    
    #split recommended_books into three parts
    part_size = (len(recommended_books) + 2) // 3
    recommended_books_1 = recommended_books[:part_size]
    recommended_books_2 = recommended_books[part_size:part_size*2]
    recommended_books_3 = recommended_books[part_size*2:]
    
    context = {
        'trending_books': trending_books,
        
        
        'recommended_books_1': recommended_books_1,
        'recommended_books_2': recommended_books_2,
        'recommended_books_3': recommended_books_3,
        
        'must_read_1': must_read_1,
        'must_read_2': must_read_2,
        'must_read_3': must_read_3,
    }
    return render(request, 'home.html', context)



def shop(request):
    books = Book.objects.all()
    halfway_index = len(books) // 2
    books_before = books[:halfway_index]
    books_after = books[halfway_index:]
    
    context = {
        'books_before': books_before,
        'books_after': books_after,
    }
    
    return render(request, 'shopbook.html', context)

    
def bookdetails(request, slug):
    try:
        book = get_object_or_404(Book, slug=slug)
        context = {
            'book': book,
           
        }
        return render(request, 'shop-single.html', context)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in product_detail view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")
    
    
    



 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
def wishlist(request):
    template = loader.get_template('account-wishlist.html')
    return HttpResponse(template.render())

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
    
            