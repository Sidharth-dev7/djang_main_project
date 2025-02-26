# models.py
from django.db import models

# User's model

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

# Garage's Model