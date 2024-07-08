
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from haystack.views import SearchView
from django.urls import re_path
from django.contrib.auth import views as auth_views




urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('book.urls', namespace='book')),
    path('book/', include('django.contrib.auth.urls')),
    path('haystack_search/', SearchView(), name='haystack_search'), 
    path('', include('paypal.standard.ipn.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete')
    
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



