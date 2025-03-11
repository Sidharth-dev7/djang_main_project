#views.py
from django.shortcuts import render, redirect
from .forms import AddForm, GForm, EditForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer, Garage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# -----------------------------------------------
#                   HOME PAGE
# -----------------------------------------------
def home(request):
    return render(request, 'Home.html')

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

# User Registration
def register(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('user_login')  # Redirect to login page after registration
    else:
        form = AddForm()
    return render(request, 'User_Registration.html', {'form': form})

# Customer Login
def user_login(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
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

        # Check the password
        if user.check_password(password):
            # Manually log in the user by setting session data
            request.session['customer_id'] = user.id
            request.session['customer_email'] = user.email
            return JsonResponse({"success": True})  # Login successful
        else:
            return JsonResponse({"success": False, "error": "Invalid email/phone or password."})

    return JsonResponse({"success": False, "error": "Invalid request method."})

def customer_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'customer_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_login')  # Redirect to login page if not logged in
    return wrapper

# User Dashboard (Protected)
@customer_login_required
def user_dashboard(request):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    return render(request, "user_dashboard.html", {'customer': customer})

# Logout
def user_logout(request):
    # Clear the session data
    request.session.flush()
    return redirect('home')  # Redirect to the home page after logout

# Edit Account (Protected)
@customer_login_required  # Use custom authentication check instead of @login_required
def edit_account(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
        if request.method == "POST":
            form = EditForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()  # Save the updated details
                return JsonResponse({"success": True})  # Return JSON response
            else:
                return JsonResponse({"success": False, "error": "Invalid form data."})  # Return JSON response
        else:
            form = EditForm(instance=customer)
        
        return render(request, 'edit_account.html', {'form': form})
    else:
        return JsonResponse({"success": False, "error": "User not logged in."})  # Return JSON response
    
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
def garage_registration(request):
    if request.method == "POST":
        form = GForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            print("Form is valid")
            print("Uploaded file:", request.FILES.get('image'))  # Debugging output
            form.save()
            return redirect('home')  # Change to your success URL
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors
    else:
        form = GForm()
    
    return render(request, 'garage_reg.html', {'form': form})

# Garage Owner Login
def garage_owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            garage = Garage.objects.get(email=email)  # Check if email exists in the Garage model
            if garage.check_password(password):
                # Manually log in the garage owner by setting session data
                request.session['garage_id'] = garage.id
                request.session['garage_email'] = garage.email
                return redirect('garage_dashboard')  # Redirect to the garage owner's dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        
        except Garage.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'garage_dashboard.html')  # Ensure you have a login template

def garage_owner_dashboard(request):
    garage_id = request.session.get('garage_id')
    if garage_id:
        garage = Garage.objects.get(id=garage_id)
        return render(request, 'garage_dashboard.html', {'garage': garage})
    else:
        return redirect('home')  # Redirect to home if not logged in

# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')