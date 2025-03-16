from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    current_request = models.ForeignKey('Request', null=True, blank=True, on_delete=models.SET_NULL)  # Change 'ServiceRequest' to 'Request'

    def mark_completed(self):
        """When a worker completes a job, reset their status and clear the current request."""
        self.status = 'available'
        self.current_request = None
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


class Car(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=20)
    auto_model = models.CharField(max_length=20)

# -----------------------------------------------
#                   REQUEST SECTION
# -----------------------------------------------

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    car_manufacturer = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.customer.first_name} {self.customer.last_name} for {self.car_manufacturer} {self.car_model}"


