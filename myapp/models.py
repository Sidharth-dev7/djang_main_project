# models.py

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# -----------------------------------------------
#                   GARAGE SECTION
# -----------------------------------------------

class Garage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed password
    address = models.TextField()
    services_offered = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    is_approved = models.BooleanField(default=False)  # Approval status

    def __str__(self):
        return self.name

# -----------------------------------------------
#                   WORKER SECTION
# -----------------------------------------------
class Worker(models.Model):
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('unavailable', 'Unavailable'),
    ]
    
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='available')
    current_request = models.ForeignKey('Request', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_worker')  # Add related_name

    # New field for worker toggle (default to True - Available)
    is_active = models.BooleanField(default=True)  # This is the toggle

    def save(self, *args, **kwargs):
        """Do not overwrite status based on toggle."""
        if self.is_active:  # If toggle is on, the worker is available
            self.status = 'available'
        elif self.current_request:  # If assigned to a request
            self.status = 'assigned'
        else:
            self.status = 'unavailable'  # If toggle is off and no request
        super().save(*args, **kwargs)

    def mark_completed(self):
        """Reset status when work is completed."""
        self.status = 'available'  # This can reset after the task is completed
        self.save()

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed password
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE,default=1)  # Link customer to garage

    def __str__(self):
        return self.email  # String representation of the user

    def set_password(self, raw_password):
        """Hash the password before saving."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password matches the hashed password."""
        return check_password(raw_password, self.password)

# -----------------------------------------------
#                  NOTIFICATION SECTION
# -----------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to the customer
    message = models.CharField(max_length=255)  # Notification message
    link = models.CharField(max_length=255)  # Link to the checkout page
    is_read = models.BooleanField(default=False)  # Whether the notification has been read
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message}"

# -----------------------------------------------
#                   REQUEST SECTION
# -----------------------------------------------
class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE)
    car_manufacturer = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')  # Add related_name

    def __str__(self):
        return f"Request from {self.customer.first_name} {self.customer.last_name} for {self.car_manufacturer} {self.car_model}"
    
# -----------------------------------------------
#            SERVICE RECORDS SECTION
# -----------------------------------------------
class ServiceRecord(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE) 
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True) 
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE) 
    completed_at = models.DateTimeField(auto_now_add=True) 
    service_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"Service Record - {self.request} - Completed on {self.completed_at}"