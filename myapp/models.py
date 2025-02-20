from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

