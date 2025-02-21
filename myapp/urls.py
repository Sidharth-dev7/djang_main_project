# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('Registration/', views.registration, name='registration'),
]