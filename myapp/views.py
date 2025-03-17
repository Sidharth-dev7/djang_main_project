# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .forms import AddForm, GForm, EditForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer,Garage, Car, Request, Worker
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.core.mail import send_mail
import json 
from django.views.decorators.csrf import csrf_exempt

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

    # Get the counts of requests for this garage
    total_requests = Request.objects.filter(garage=garage).count()
    pending_count = Request.objects.filter(garage=garage, status='pending').count()
    approved_count = Request.objects.filter(garage=garage, status='approved').count()
    rejected_count = Request.objects.filter(garage=garage, status='rejected').count()

    return render(request, 'garage_dashboard.html', {
        'garage': garage,
        'total_requests': total_requests,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    })


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
    cars = Car.objects.filter(owner_id=request.session.get('customer_id'))  # Fetch user cars
    
    return render(request, "garage_view.html", {
        'cr': cr,
        'cars': cars,
        'is_logged_in': 'customer_id' in request.session
    })

def pending_requests(request):
    garage_id = request.session.get('garage_id')
    if not garage_id:
        return redirect('garage_owner_login')

    garage = Garage.objects.get(id=garage_id)
    pending_requests = Request.objects.filter(garage=garage, status='pending')

    return render(request, 'pending_requests.html', {'pending_requests': pending_requests})

def update_request_status(request, request_id, status):
    req = get_object_or_404(Request, id=request_id)

    if status == "Rejected":
        req.status = "Rejected"
        req.save()
        return redirect('pending_requests')

    if status == "Approved" and req.worker:
        req.status = "Approved"
        req.save()
        return redirect('pending_requests')

    return redirect('pending_requests')

# -----------------------------------------------
#             LOGIN & REGISTRATION SELECTION
# -----------------------------------------------
def login_selection(request):
    return render(request, 'login_selection.html')

def register_selection(request):
    return render(request, 'register_selection.html')

# -----------------------------------------------
#                   EMAIL
# -----------------------------------------------

def request_assistance(request, garage_id):
    garage = get_object_or_404(Garage, id=garage_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the JSON data from JavaScript
            car_manufacturer = data.get('car_manufacturer')
            car_model = data.get('car_model')
            issue_description = data.get('issue_description')

            if not car_manufacturer or not car_model or not issue_description:
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

            # Check if user is logged in (session-based check)
            customer_id = request.session.get('customer_id')
            if not customer_id:
                return JsonResponse({'success': False, 'message': 'User not logged in'}, status=403)

            customer = get_object_or_404(Customer, id=customer_id)

            # Create the new request in the database
            new_request = Request.objects.create(
                customer=customer,
                garage=garage,
                car_manufacturer=car_manufacturer,
                car_model=car_model,
                issue_description=issue_description,
                status='pending'  # Initially, the status is 'pending'
            )

            # Prepare the email content
            subject = "New Assistance Request"
            message = f"""
            Hello {garage.owner_name},

            You have received a new assistance request from {customer.first_name} {customer.last_name}.

            Car Manufacturer: {car_manufacturer}
            Car Model: {car_model}
            Issue: {issue_description}

            Contact User:
            Name: {customer.first_name} {customer.last_name}
            Phone: {customer.contact}
            Email: {customer.email}

            Please respond promptly to assist the user.

            Best regards,
            Car Breakdown Service
            """

            # Send the email to the garage owner
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Sender email
                [garage.email],  # Recipient email (garage owner)
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Request sent successfully!'})

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


# -----------------------------------------------
#             WORKERS SECTION
# -----------------------------------------------

def manage_workers(request):
    """Displays workers for the logged-in garage owner and allows adding/removing workers."""
    garage_id = request.session.get('garage_id')
    if not garage_id:
        return redirect('garage_owner_login')

    garage = Garage.objects.get(id=garage_id)
    workers = Worker.objects.filter(garage=garage)  # Fetch all workers of this garage

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        if name and phone:
            Worker.objects.create(garage=garage, name=name, phone=phone)
            messages.success(request, "Worker added successfully!")
            return redirect('manage_workers')  # Refresh page after adding worker

    return render(request, 'manage_worker.html', {'garage': garage, 'workers': workers})

def add_worker(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")  # Get the email from the form
        garage_id = request.session.get('garage_id')

        if not garage_id:
            return redirect('garage_owner_login')  # Ensure only logged-in garage owners can add workers
        
        garage = Garage.objects.get(id=garage_id)

        if Worker.objects.filter(phone=phone, garage=garage).exists():
            messages.error(request, "Worker with this phone number already exists.")
        else:
            # Now saving the email along with name, phone, and garage
            Worker.objects.create(name=name, phone=phone, email=email, garage=garage)
            messages.success(request, "Worker added successfully.")

    return redirect("manage_workers")

def remove_worker(request, worker_id):
    """Deletes a worker if the logged-in garage owner owns them."""
    garage_id = request.session.get('garage_id')
    if not garage_id:
        return redirect('garage_owner_login')

    worker = get_object_or_404(Worker, id=worker_id, garage_id=garage_id)
    worker.delete()
    messages.success(request, "Worker removed successfully!")
    return redirect('manage_workers')

def get_available_workers(request, request_id):
    """Fetch available workers for a specific service request."""
    garage_id = request.session.get('garage_id')
    if not garage_id:
        return JsonResponse({'success': False, 'message': "Not authorized"}, status=403)

    workers = Worker.objects.filter(garage_id=garage_id, status='available').values('id', 'name')

    if workers.exists():
        return JsonResponse({'success': True, 'workers': list(workers)})
    else:
        return JsonResponse({'success': False, 'message': "No workers available"}, status=400)


def assign_worker(request, request_id):
    if request.method == "POST":
        garage_id = request.session.get('garage_id')
        if not garage_id:
            return JsonResponse({'success': False, 'message': "Not authorized"}, status=403)

        service_request = get_object_or_404(Request, id=request_id, garage_id=garage_id)
        worker_id = request.POST.get('worker_id')
        worker = Worker.objects.filter(id=worker_id, garage_id=garage_id, status='available').first()

        if not worker:
            return JsonResponse({'success': False, 'message': "Worker not available"}, status=400)

        worker.status = 'assigned'
        worker.current_request = service_request
        worker.save()

        service_request.status = 'approved'  # Do NOT auto-approve, we will handle this in frontend
        service_request.save()

        return JsonResponse({
            'success': True,
            'message': f"Worker {worker.name} assigned successfully!",
            'request_details': {
                'customer': service_request.customer.first_name + " " + service_request.customer.last_name,
                'car': f"{service_request.car_manufacturer} - {service_request.car_model}",
                'issue': service_request.issue_description,
                'status': service_request.status
            }
        })

    return JsonResponse({'success': False, 'message': "Invalid request method"}, status=400)
def worker_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            # Find worker by email and phone together
            worker = Worker.objects.get(email=email, phone=phone)

            # If worker exists, create a session and redirect
            request.session['worker_id'] = worker.id  
            return redirect('worker_dashboard')  
        except Worker.DoesNotExist:
            messages.error(request, "Invalid email or phone number.")

    return render(request, 'login_selection.html')


def worker_dashboard(request):
    if 'worker_id' in request.session:  # Check if worker is logged in
        worker = Worker.objects.get(id=request.session['worker_id'])
        return render(request, 'worker_dashboard.html', {'worker': worker})
    return redirect('worker_login')  # Redirect if not logged in

@csrf_exempt
def update_worker_status(request):
    """Updates worker availability toggle in the database."""
    if request.method == "POST":
        data = json.loads(request.body)
        worker_id = data.get("worker_id")
        is_active = data.get("is_active")

        try:
            worker = Worker.objects.get(id=worker_id)
            worker.is_active = is_active  # Update the toggle status
            worker.save()  # Save the updated status in the database
            return JsonResponse({"success": True, "status": worker.status})
        except Worker.DoesNotExist:
            return JsonResponse({"success": False, "error": "Worker not found"}, status=404)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



def get_worker_status(request, worker_id):
    """Returns the current status of a worker (available/unavailable)."""
    try:
        worker = Worker.objects.get(id=worker_id)
        return JsonResponse({"status": worker.status})
    except Worker.DoesNotExist:
        return JsonResponse({"error": "Worker not found"}, status=404)


def get_workers(request, request_id):
    """Fetch all workers dynamically with correct availability status."""
    workers = Worker.objects.all()

    worker_data = []
    for worker in workers:
        # Determine correct status dynamically
        if not worker.is_active:
            status = "unavailable"  # Toggle is OFF, mark worker as unavailable
        elif worker.current_request:
            status = "assigned"  # Worker is currently assigned
        else:
            status = "available"  # Worker is free and active

        worker_data.append({
            "id": worker.id,
            "name": worker.name,
            "status": status
        })

    return JsonResponse(worker_data, safe=False)

