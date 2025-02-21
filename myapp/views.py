# views.py
from django.shortcuts import render, redirect
from .forms import AddForm
from .models import Customer, Car

# Create your views here.

def registration(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration')
    else:
        form = AddForm()
    
    return render(request, 'User_Registration.html', {'form': form})