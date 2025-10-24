from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    ACTIVITY_LEVEL = (
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('active', 'Active'),
        ('very-active', 'Very active'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    goal = models.CharField(max_length=200, null=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            return full_name or self.user.username
        return "Unknown Customer"




class Progress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    weight = models.FloatField(null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)