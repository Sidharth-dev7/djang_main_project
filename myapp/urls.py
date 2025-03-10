# urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def check_login(request):
    is_authenticated = 'customer_id' in request.session  # Check for custom session variable
    return JsonResponse({"is_authenticated": is_authenticated})

urlpatterns = [
    # -----------------------------------------------
    #                   USER PATHS
    # -----------------------------------------------
    path('', views.home, name='home'),
    path('user_registration/', views.register, name='user_reg'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path("check-login/", check_login, name="check_login"),
    path("logout/", views.user_logout, name="logout"),
    path("edit-account/", views.edit_account, name="edit_account"),
    path('normal-user-login/', views.normal_user_login, name='normal_user_login'),

    # -----------------------------------------------
    #                GARAGE OWNER PATHS
    # -----------------------------------------------
    path('garage_registration/', views.garage_registration, name='garage_reg'),
    path('garage-owner-login/', views.garage_owner_login, name='garage_owner_login'),
    path('ownerdashboard/', views.garage_owner_dashboard, name='garage_dashboard'),

    # -----------------------------------------------
    #               COMMON LOGIN & REGISTER
    # -----------------------------------------------
    path('register/', views.register_selection, name='register_selection'),
    path('login/', views.login_selection, name='login_selection'),
]

if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)