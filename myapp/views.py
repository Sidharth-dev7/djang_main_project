# views.py
from django.shortcuts import render, redirect
from .forms import AddForm, GForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

# -----------------------------------------------
#                   HOME PAGE
# -----------------------------------------------
def home(request):
    return render(request, 'Home.html')

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

#User Registration
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

def normal_user_registration(request):
    return render(request, 'User_Registration.html')

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

# -----------------------------------------------
#                   GARAGE SECTION
# -----------------------------------------------

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

def garage_registration(request):
    return render(request, 'garage_reg.html')

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

def garage_owner_dashboard(request):
    return render(request, 'garage_dashboard.html')

# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')
