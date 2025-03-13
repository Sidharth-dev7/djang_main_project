#models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed password

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
    # reg_plate = models.CharField(max_length=10)

# -----------------------------------------------
#                   GARAGE SECTION
# -----------------------------------------------
# Garage's Model
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