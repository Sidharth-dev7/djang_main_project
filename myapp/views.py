# views.py
from django.shortcuts import render, redirect
from .forms import AddForm, GForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer,Garage
from django.contrib.auth.hashers import check_password, make_password

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
            user.save()  # Now save the user with the hashed password
            return redirect('user_dashboard')
    else:
        form = AddForm()
    
    return render(request, 'User_Registration.html', {'form': form})

def user_dashboard(request):
    cr=Garage.objects.all()
    return render(request, "user_dashboard.html",{'cr'  :cr})


def user_login(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_phone")
        password = request.POST.get("password")

        customer = Customer.objects.filter(email=email_or_phone).first() or \
                   Customer.objects.filter(contact=email_or_phone).first()

        if customer and check_password(password, customer.password):  
            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.first_name
            return JsonResponse({"success": True, "redirect_url": "/user-dashboard/"})
        else:
            return JsonResponse({"success": False, "message": "Invalid email/phone or password."})

    return JsonResponse({"success": False, "message": "Invalid request."})

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

# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')
