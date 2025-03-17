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
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path("check-login/", check_login, name="check_login"),
    path("user-logout/", views.user_logout, name="user_logout"), 
    path("edit-account/", views.edit_account, name="edit_account"),
    path('normal-user-login/', views.normal_user_login, name='normal_user_login'),
    path('garage/<int:pk>/', views.garage_detail, name='garage_detail'),

    # -----------------------------------------------
    #                GARAGE OWNER PATHS
    # -----------------------------------------------
    path('garage_registration/', views.garage_registration, name='garage_reg'),
    path('garage-owner-login/', views.garage_owner_login, name='garage_owner_login'),
    path('ownerdashboard/', views.garage_owner_dashboard, name='garage_dashboard'),
    path('edit/', views.edit_garage, name='edit_garage'),
    path('logout/', views.logout_view, name='logout'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),

    # -----------------------------------------------
    #               COMMON LOGIN & REGISTER
    # -----------------------------------------------
    path('register/', views.register_selection, name='register_selection'),
    path('login/', views.login_selection, name='login_selection'),

    # -----------------------------------------------
    #               EMAIL
    # -----------------------------------------------
    path('garage/<int:garage_id>/request/', views.request_assistance, name='request_assistance'),

    # -----------------------------------------------
    #               WORKERS
    # -----------------------------------------------
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('get-workers/<int:request_id>/', views.get_workers, name='get_workers'),
    path('worker_login/', views.worker_login, name='worker_login'),
    path('update_worker_status/', views.update_worker_status, name='update_worker_status'),
    path("get_worker_status/<int:worker_id>/", views.get_worker_status, name="get_worker_status"),
    path('manage-workers/', views.manage_workers, name='manage_workers'),
    path('add-worker/', views.add_worker, name='add_worker'),
    path('remove-worker/<int:worker_id>/', views.remove_worker, name='remove_worker'),
    path('assign_worker/<int:request_id>/', views.assign_worker, name='assign_worker'),
    path('get_available_workers/<int:request_id>/', views.get_available_workers, name='get_available_workers'),
    path('update-request-status/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),
    path('get_assigned_request/<int:worker_id>/', views.get_assigned_request, name='get_assigned_request'),
    path('mark_request_completed/<int:request_id>/', views.mark_request_completed, name='mark_request_completed'),

    # -----------------------------------------------
    #               CHECKOUT
    # -----------------------------------------------
    # path("checkout/<int:job_id>/", views.checkout, name="checkout"),
    
    # -----------------------------------------------
    #               SERVICE RECORDS
    # -----------------------------------------------
    path('service-records/', views.service_records, name='service_records'),
]

if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)