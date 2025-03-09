# views.py
from django.shortcuts import render, redirect
from .forms import AddForm, GForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer,Garage
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .forms import AddForm 

# -----------------------------------------------
#                   HOME PAGE
# -----------------------------------------------
def home(request):
    return render(request, 'Home.html')

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

User = get_user_model()

def custom_authenticate(email_or_contact, password):
    try:
        user = User.objects.get(email=email_or_contact)  # Try email first
    except User.DoesNotExist:
        try:
            user = User.objects.get(contact=email_or_contact)  # Try phone number
        except User.DoesNotExist:
            return None  # User not found
    
    if user.check_password(password):  # Check if password is correct
        return user
    return None

#User Registration
def register(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.password = make_password(user.password)  # Hash the password
            user.save()  # Save the user with the hashed password

            # Log in the user after registration
            login(request, user)

            # Redirect to the user dashboard
            return redirect('user_dashboard')
    else:
        form = AddForm()
    
    return render(request, 'User_Registration.html', {'form': form})

# Customer Login
def user_login(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_phone")
        password = request.POST.get("password")

        # Try to find the user by email or phone
        try:
            user = Customer.objects.get(email=email_or_phone)
        except Customer.DoesNotExist:
            try:
                user = Customer.objects.get(contact=email_or_phone)
            except Customer.DoesNotExist:
                return JsonResponse({"success": False, "error": "Invalid email/phone or password."})

        # Authenticate the user
        user = authenticate(request, username=user.email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})  # Login successful
        else:
            return JsonResponse({"success": False, "error": "Invalid email/phone or password."})

    return JsonResponse({"success": False, "error": "Invalid request method."})

def user_dashboard(request):
    return render(request, "user_dashboard.html")

def check_login(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated})

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page after logout

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
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            garage = Garage.objects.get(email=email)  # Check if email exists in the Garage model
            user = authenticate(request, username=garage.owner_name, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('garage_dashboard')  # Redirect to the garage owner's dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        
        except Garage.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'garage_dashboard.html')  # Ensure you have a login template

def garage_owner_dashboard(request):
    return render(request, 'garage_dashboard.html')

# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')
