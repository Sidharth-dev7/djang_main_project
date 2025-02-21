from django.shortcuts import render
from .models import Customer, Car

# Create your views here.

def registration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"