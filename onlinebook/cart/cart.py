from django.conf import settings
from django.shortcuts import get_object_or_404
from book.models import Book

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    
    def __iter__(self):
        book_slugs = self.cart.keys()
        books = Book.objects.filter(slug__in=book_slugs)
        
        for book in books:
            self.cart[str(book.slug)]['book'] = book
        
        for item in self.cart.values():
            item['book'] = Book.objects.get(slug=item['slug'])
            
            yield item
            
              
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())     
  

    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def add(self, book_slug, quantity=1, update_quantity=False):
        book_slug = str(book_slug)
        
        if book_slug not in self.cart:
            self.cart[book_slug] = {'quantity': 1, 'slug': book_slug}
            
        if update_quantity:
            self.cart[book_slug]['quantity'] += int(quantity)   
            
            if self.cart[book_slug]['quantity'] == 0:
                self.remove(book_slug)
        self.save()
        
    def remove(self, book_slug):
        if book_slug in self.cart:
            del self.cart[book_slug]
            self.save()    
            
            
    def get_total_cost(self):
        return sum(item['quantity'] * item['book'].price  for item in self.cart.values())                
