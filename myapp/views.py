from django.shortcuts import render, redirect
from .forms import AddForm, GForm, EditForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer, Garage
from django.contrib.auth.hashers import make_password, check_password  # Ensure password hashing
from django.contrib.auth.decorators import login_required

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
            user.password = make_password(form.cleaned_data['password'])  # Hash password correctly
            user.save()
            return redirect('user_login')  # Redirect to login page after registration
    else:
        form = AddForm()
    return render(request, 'User_Registration.html', {'form': form})

# Normal User Login (Allows login via email or contact number)
def normal_user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')  # This can be email or phone number
        password = request.POST.get('password')

        try:
            # Check if the identifier exists in the database
            user = Customer.objects.filter(email=identifier).first() or Customer.objects.filter(contact=identifier).first()
            
            if user and check_password(password, user.password):  # Verify password
                request.session['customer_id'] = user.id  # Store user session
                return redirect('user_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, "Invalid email/contact number or password.")

        except Customer.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'normal_user_login.html')

# Customer Login Required Decorator
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
    request.session.flush()  # Clear session data
    return redirect('home')  # Redirect to home page after logout

# Edit Account (Protected)
@customer_login_required
def edit_account(request):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id)

    if request.method == "POST":
        form = EditForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid form data."})

    form = EditForm(instance=customer)
    return render(request, 'edit_account.html', {'form': form})

# -----------------------------------------------
#                   GARAGE SECTION
# -----------------------------------------------

# Garage Registration
def garage_registration(request):
    if request.method == "POST":
        form = GForm(request.POST, request.FILES)
        if form.is_valid():
            garage = form.save(commit=False)
            garage.password = make_password(form.cleaned_data['password'])  # Hash password
            garage.save()
            return redirect('home')  # Redirect after successful registration
    else:
        form = GForm()
    
    return render(request, 'garage_reg.html', {'form': form})

# Garage Owner Login
def garage_owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            garage = Garage.objects.get(email=email)  # Check if email exists

            if check_password(password, garage.password):  # Verify password
                request.session['garage_id'] = garage.id
                request.session['garage_email'] = garage.email
                return redirect('garage_dashboard')  # Redirect to garage dashboard
            else:
                messages.error(request, "Invalid email or password.")

        except Garage.DoesNotExist:
            messages.error(request, "Garage not found.")

    return render(request, 'garage_login.html')  # Ensure correct template

# Garage Owner Dashboard
def garage_owner_dashboard(request):
    garage_id = request.session.get('garage_id')
    if garage_id:
        garage = Garage.objects.get(id=garage_id)
        return render(request, 'garage_dashboard.html', {'garage': garage})
    else:
        return redirect('home')  # Redirect if not logged in

# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')
