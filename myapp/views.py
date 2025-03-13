# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .forms import AddForm, GForm, EditForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer,Garage
from django.contrib.auth.hashers import check_password, make_password

# -----------------------------------------------
#                   HOME PAGE
# -----------------------------------------------
def home(request):
    is_logged_in = 'customer_id' in request.session  # Check if user is logged in
    return render(request, 'Home.html', {'is_logged_in': is_logged_in})


# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

# User Registration
def register(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash password
            user.save()

            # Auto-login: Store user session
            request.session['customer_id'] = user.id  

            return redirect('user_dashboard')  # Redirect to dashboard instead of login page
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
def user_dashboard(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('user_login')

    customer = Customer.objects.get(id=customer_id)
    cr = Garage.objects.filter(is_approved=True)  # Show only approved garages

    return render(request, "user_dashboard.html", {
        'customer': customer, 
        'cr': cr, 
        'is_logged_in': True
    })


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
            garage.is_approved = False  # Default to unapproved
            garage.save()
            return render(request, 'garage_reg.html', {'form': GForm(), 'show_confirmation': True})  
    else:
        form = GForm()
    
    return render(request, 'garage_reg.html', {'form': form})


# Garage Owner Login
def garage_owner_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            garage = Garage.objects.get(email=email)
            if garage.password == password:  # Replace with hashed password check in production
                request.session['garage_id'] = garage.id  # Store session data
                return redirect('garage_dashboard')
            else:
                messages.error(request, "Invalid password.")
        except Garage.DoesNotExist:
            messages.error(request, "Garage not found.")

    return render(request, 'login_selection.html')

def garage_owner_dashboard(request):
    garage_id = request.session.get('garage_id')
    if not garage_id:
        return redirect('garage_owner_login')

    garage = Garage.objects.get(id=garage_id)
    return render(request, 'garage_dashboard.html', {'garage': garage})

def edit_garage(request):
    garage_id = request.session.get('garage_id')
    if not garage_id:
        return redirect('garage_owner_login')

    garage = Garage.objects.get(id=garage_id)

    if request.method == "POST":
        form = GForm(request.POST, request.FILES, instance=garage)
        if form.is_valid():
            form.save()
            return redirect('garage_dashboard')
    else:
        form = GForm(instance=garage)

    return render(request, 'garage_edit.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def garage_detail(request, pk):
    cr = Garage.objects.get(id=pk)
    is_logged_in = 'customer_id' in request.session  # Check if user is logged in
    return render(request, "garage_view.html", {'cr': cr, 'is_logged_in': is_logged_in})
# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')
