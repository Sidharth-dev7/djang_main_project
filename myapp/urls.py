# urls.py
from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home, name='home'),
    path('registration/', views.register, name='registration'),
    path('garage/', views.G_reg, name='garage_reg'),
]