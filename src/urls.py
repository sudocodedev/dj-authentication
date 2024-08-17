from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home_page, name="home-page"), # home page    
    
    path('account/', include("accounts.urls")), # Authentication & Account creation

    path('auth/', include('social_django.urls', namespace='social')), # social auth
]
