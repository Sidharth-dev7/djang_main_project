# urls.py
from django.urls import path
from . import views

urlpatterns = [
   
   # User's path
    path('', views.home, name='home'),
    path('Registration/', views.register, name='registration'),
    path('find-garages/', views.user_dashboard, name='user_dashboard'),

   # Garage's path 
    path('garage/', views.G_reg, name='garage_reg'),
]