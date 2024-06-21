from .models import BooksCategory

def categories_processor(request):
    categories = BooksCategory.objects.all()
    return {
        'categories': categories
    }
