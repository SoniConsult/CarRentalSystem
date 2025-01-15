from django.db import models

# Create your models here.

from django.db import models

class Car(models.Model):
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    registration_number = models.CharField(
         max_length=15,  # Specify max_length to avoid errors
        unique=True,
    )
    seating_capacity = models.IntegerField()