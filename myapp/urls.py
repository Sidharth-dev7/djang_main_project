# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
   # User's path
    path('', views.home, name='home'),
    path('Registration/', views.register, name='registration'),
    path('find-garages/', views.user_dashboard, name='user_dashboard'),


   # Garage's path 
    path('garage/', views.G_reg, name='garage_reg'),
    path('login/', views.login_selection, name='login_selection'),
    path('garage-owner-login/', views.garage_owner_login, name='garage_owner_login'),
    path('normal-user-login/', views.normal_user_login, name='normal_user_login'),
    path('ownerdashboard/', views.garage_owner_dashboard, name='garage_dashboard')
]

if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)