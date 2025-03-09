# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

# Custom User Manager (Simplified)
class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a customer with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, **extra_fields)  # Create the user
        user.set_password(password)  # Hash the password
        user.save(using=self._db)  # Save the user to the database
        return user

# Custom User Model
class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # This will store the hashed password

    # Custom User Manager
    objects = CustomerManager()

    # Use email as the username field (instead of the default 'username')
    USERNAME_FIELD = "email"

    # Required fields for creating a user (other than USERNAME_FIELD and password)
    REQUIRED_FIELDS = ["first_name", "last_name", "contact"]

    def __str__(self):
        return self.email  # String representation of the user

class Car(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=20)
    auto_model = models.CharField(max_length=20)
    reg_plate = models.CharField(max_length=10)

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

    def __str__(self):
        return self.name