# views.py
from django.shortcuts import render, redirect
from .forms import AddForm,GForm
from .models import Customer, Car,Garage

# Create your views here.

def home(request):
    return render(request, 'Home.html')

def register(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration')
    else:
        form = AddForm()
    
    return render(request, 'User_Registration.html', {'form': form})


def G_reg(request):
    if request.method == "POST":
        form = GForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GForm()
    
    return render(request, 'garage_reg.html', {'form': form})