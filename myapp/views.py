# views.py
from django.shortcuts import render, redirect
from .forms import AddForm, GForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

# Home Page
def home(request):
    return render(request, 'Home.html')

# User Registration
def register(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            form.save()  # Passwords are automatically hashed
            return redirect('user_dashboard')
    else:
        form = AddForm()
    
    return render(request, 'User_Registration.html', {'form': form})

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('email_phone')  # Use get() to avoid KeyError
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})  # Redirect to home
        
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# Garage Registration
def G_reg(request):
    if request.method == "POST":
        form = GForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GForm()
    
    return render(request, 'garage_reg.html', {'form': form})

# Login Selection Page
def login_selection(request):
    return render(request, 'login_selection.html')

# Garage Owner Login
def garage_owner_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('garage_owner_dashboard')  # Update this to the actual dashboard URL
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'garage_owner_login.html')

# Normal User Login
def normal_user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('normal_user_dashboard')  # Update this to the actual dashboard URL
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'normal_user_login.html')



def garage_owner_dashboard(request):
    return render(request, 'garage_dashboard.html')