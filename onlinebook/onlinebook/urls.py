
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from haystack.views import SearchView



urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('book.urls', namespace='book')),
    path('book/', include('django.contrib.auth.urls')),
    path('haystack_search/', SearchView(), name='haystack_search'), 
    
    path('', include('paypal.standard.ipn.urls')),
]

# Only serve media files during development


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]



