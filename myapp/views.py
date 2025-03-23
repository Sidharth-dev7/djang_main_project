# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .forms import AddForm, GForm, EditForm
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer,Garage, Request, Worker, ServiceRecord
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.core.mail import send_mail
import json 
from django.views.decorators.csrf import csrf_exempt
from .models import Request, Notification
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse, Http404
import os, logging

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

    return render(request, 'login_selection.html')

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


def get_notifications(request):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        notifications = Notification.objects.filter(user_id=customer_id, is_read=False).order_by('-created_at')
        notifications_data = [{
            'id': notification.id,  # Include the ID field
            'message': notification.message,
            'link': f"{notification.link}?notification_id={notification.id}"  # Add notification_id to the link
        } for notification in notifications]
        return JsonResponse({'notifications': notifications_data})
    return JsonResponse({'notifications': []})

import logging
logger = logging.getLogger(__name__)

def mark_notification_read(request, notification_id):
    if request.method == "POST":
        try:
            # Fetch the notification
            notification = Notification.objects.get(id=notification_id)

            # Mark the notification as read
            notification.is_read = True
            notification.save()

            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse({"success": False, "error": "Notification not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

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
    
    return render(request, "garage_view.html", {
        'cr': cr,
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
#             GARAGE WORKERS SECTION
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
        # Debugging: Print the request ID
        print(f"Assigning worker to request ID: {request_id}")

        # Parse the JSON payload
        try:
            data = json.loads(request.body)
            worker_id = data.get('worker_id')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "Invalid JSON data"}, status=400)

        # Debugging: Print the worker ID
        print(f"Worker ID: {worker_id}")

        # Get the garage ID from the session
        garage_id = request.session.get('garage_id')
        if not garage_id:
            return JsonResponse({'success': False, 'message': "Not authorized"}, status=403)

        # Fetch the service request based on the request ID and garage ID
        service_request = get_object_or_404(Request, id=request_id, garage_id=garage_id)

        # Fetch the worker who is available
        worker = Worker.objects.filter(id=worker_id, garage_id=garage_id, status='available').first()

        # Debugging: Print the worker object
        print(f"Worker: {worker}")

        # Check if the worker is available
        if not worker:
            return JsonResponse({'success': False, 'message': "Worker not available"}, status=400)

        # Assign the worker to the service request
        service_request.worker = worker  # Update the request to link to the worker
        worker.current_request = service_request  # Update the worker to link to the request
        worker.status = 'assigned'  # Update the worker's status to 'assigned'

        # Save the changes to the worker and the service request
        worker.save()  # Save the updated worker
        service_request.save()  # Save the updated request

        # Debugging: Print the updated request and worker
        print(f"Updated Request: {service_request}")
        print(f"Updated Worker: {worker}")

        # Prepare the response data
        return JsonResponse({
            'success': True,
            'message': f"Worker {worker.name} assigned successfully!",
            'request_id': service_request.id,
            'worker_id': worker.id,
            'request_details': {
                'customer': f"{service_request.customer.first_name} {service_request.customer.last_name}",
                'car': f"{service_request.car_manufacturer} - {service_request.car_model}",
                'issue': service_request.issue_description,
                'status': service_request.status  # This will reflect the updated status
            }
        })

    # If the request method is not POST, return an error
    return JsonResponse({'success': False, 'message': "Invalid request method"}, status=400)

# -----------------------------------------------
#             WORKERS SECTION
# -----------------------------------------------

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

def get_assigned_request(request, worker_id):
    """Fetch the request assigned to the worker."""
    try:
        worker = Worker.objects.get(id=worker_id)
        
        # Check if the worker has an assigned request
        if worker.current_request:
            assigned_request = worker.current_request
            return JsonResponse({
                "success": True,
                "request_details": {
                    "customer": f"{assigned_request.customer.first_name} {assigned_request.customer.last_name}",
                    "car": f"{assigned_request.car_manufacturer} - {assigned_request.car_model}",
                    "issue": assigned_request.issue_description,
                    "status": assigned_request.status
                }
            })
        else:
            # No assigned request
            return JsonResponse({"success": True, "request_details": None})
    except Worker.DoesNotExist:
        return JsonResponse({"success": False, "error": "Worker not found"}, status=404)

import logging

logger = logging.getLogger(__name__)

def mark_request_completed(request, request_id):
    """Mark a request as completed and notify the user via email and notification."""
    if request.method == "POST":
        try:
            # Fetch the request
            service_request = Request.objects.get(id=request_id)

            # Mark the request as completed
            service_request.status = "completed"
            service_request.save()

            # Update the worker's status
            worker = service_request.worker
            worker.current_request = None
            worker.status = "available"
            worker.save()

            # Send email to the user
            subject = 'Your Request Has Been Completed'
            message = (
                f"Hello {service_request.customer.first_name},\n\n"
                f"We are pleased to inform you that your request for {service_request.car_manufacturer} {service_request.car_model} "
                f"with the issue '{service_request.issue_description}' has been marked as completed.\n\n"
                f"Thank you for using our service!\n\n"
                f"Best regards,\n"
                f"The Garage Team"
            )
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [service_request.customer.email]  # Ensure the Customer model has an email field

            send_mail(subject, message, email_from, recipient_list)

            # Create a notification for the user
            Notification.objects.create(
                user=service_request.customer,  # Link to the customer
                message=f"Your request for {service_request.car_manufacturer} {service_request.car_model} has been completed.",
                link=f"/checkout/{service_request.id}/",  # Link to the checkout page
                is_read=False
            )

            return JsonResponse({
                "success": True,
                "message": "Request marked as completed successfully!",
                "request_id": service_request.id,
                "worker_id": worker.id
            })
        except Request.DoesNotExist:
            logger.error(f"Request with ID {request_id} not found.")
            return JsonResponse({"success": False, "error": "Request not found"}, status=404)
        except Exception as e:
            logger.error(f"Error marking request as completed: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

# -----------------------------------------------
#            SERVICE RECORDS SECTION
# -----------------------------------------------

@customer_login_required
def service_records(request):
    """Display service history for the logged-in user."""
    customer_id = request.session.get('customer_id')
    logger.info(f"Fetching service records for customer ID: {customer_id}")
    
    records = ServiceRecord.objects.filter(request__customer_id=customer_id).order_by('-completed_at')
    logger.info(f"Records fetched: {records}")

    return render(request, 'service_records.html', {'records': records})

logger = logging.getLogger(__name__)
@csrf_exempt
def confirm_payment(request, request_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Received payload: {data}")  # Debugging: Log the payload

            payment_method = data.get("payment_method")
            notification_id = data.get("notification_id")  # Get the notification_id from the request

            if not payment_method:
                logger.error("Payment method is required")  # Debugging: Log missing payment method
                return JsonResponse({"success": False, "error": "Payment method is required"}, status=400)

            # Fetch the request
            service_request = Request.objects.get(id=request_id)
            logger.info(f"Fetched request: {service_request}")  # Debugging: Log the fetched request

            # Mark the request as completed
            service_request.status = "completed"
            service_request.save()
            logger.info("Request marked as completed")  # Debugging: Log request completion

            # Check if a ServiceRecord already exists for this request
            service_record, created = ServiceRecord.objects.get_or_create(
                request=service_request,
                defaults={
                    "worker": service_request.worker,
                    "garage": service_request.garage,
                    "service_price": 50.00  # Replace with actual price logic
                }
            )
            logger.info(f"ServiceRecord {'created' if created else 'updated'}: {service_record}")  # Debugging: Log ServiceRecord creation/update

            # Generate the invoice PDF (your existing logic)

            # Mark the notification as read
            if notification_id:
                try:
                    notification = Notification.objects.get(id=notification_id)
                    notification.is_read = True
                    notification.save()
                    logger.info(f"Notification marked as read: {notification}")  # Debugging: Log notification update
                except Notification.DoesNotExist:
                    logger.warning(f"Notification with ID {notification_id} not found")  # Debugging: Log missing notification

            return JsonResponse({"success": True, "message": "Payment confirmed and invoice generated!"})
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")  # Debugging: Log JSON decode error
            return JsonResponse({"success": False, "error": "Invalid JSON payload"}, status=400)
        except Exception as e:
            logger.error(f"Error in confirm_payment: {str(e)}")  # Debugging: Log general error
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

def download_invoice(request, record_id):
    try:
        service_record = ServiceRecord.objects.get(id=record_id)
        if service_record.invoice_pdf:
            file_path = service_record.invoice_pdf.path
            with open(file_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            raise Http404("Invoice not found")
    except ServiceRecord.DoesNotExist:
        raise Http404("Service record not found")

# -----------------------------------------------
#                   CHECKOUT SECTION
# -----------------------------------------------

def checkout(request, job_id):
    try:
        # Fetch the completed request
        service_request = Request.objects.get(id=job_id, status="completed")
        return render(request, 'checkout.html', {
            'job_id': job_id,
            'service_request': service_request
        })
    except Request.DoesNotExist:
        return redirect('user_dashboard')  # Redirect to dashboard if the request is invalid

def check_request_status(request, request_id):
    # Logic to check if the request is completed
    # This could be a database query to check the status of the request
    request_completed = ...  # Replace with your logic to check if the request is completed

    return JsonResponse({'completed': request_completed})

