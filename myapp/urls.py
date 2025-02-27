# urls.py
from django.urls import path
from . import views
from .views import login_selection, garage_owner_login, normal_user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('', views.home, name='home'),
    path('registration/', views.register, name='registration'),
    path('garage/', views.G_reg, name='garage_reg'),
    path('login/', login_selection, name='login_selection'),
    path('garage-owner-login/', garage_owner_login, name='garage_owner_login'),
    path('normal-user-login/', normal_user_login, name='normal_user_login'),
    path('ownerdashboard/', views.garage_owner_dashboard, name='garage_dashboard')
]

if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)