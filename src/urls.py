from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home_page, name="home-page"), # home page    
    
    path('account/', include("accounts.urls")), # Authentication & Account creation

    path('auth/', include('social_django.urls', namespace='social')), # social auth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
