# urls.py
from django.urls import path
from . import views

urlpatterns = [
   
   # User's path
    path('', views.home, name='home'),
    path('Registration/', views.register, name='registration'),

   # Garage's path 
    #path('registration/', views.register, name='registration'),
    path('garage/', views.G_reg, name='garage_reg'),
]