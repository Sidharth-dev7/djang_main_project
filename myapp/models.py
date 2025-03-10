# models.py
from django.db import models

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Car(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=20)
    auto_model = models.CharField(max_length=20)
    reg_plate = models.CharField(max_length=10)

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

    def __str__(self):
        return self.name