# urls.py
from django.urls import path
from . import views

urlpatterns = [
   
   # User's path
    path('', views.home, name='home'),
    path('Registration/', views.registration, name='registration'),

   # Garage's path 
]