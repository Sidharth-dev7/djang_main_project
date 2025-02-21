from django.shortcuts import render
from .models import Customer, Car

# Create your views here.

def registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')