from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Book, BooksCategory, Author, Profile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, CustomUserAdmin)  # Register User with custom admin


# Register your models here.
@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    
admin.site.register(BooksCategory)
admin.site.register(Author)
admin.site.register(Profile)



