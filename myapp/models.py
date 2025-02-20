from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=20)
    auto_model = models.CharField(max_length=20)
    reg_plate = models.CharField(max_length=10)