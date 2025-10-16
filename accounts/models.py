from django.db import models

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


    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    goal = models.CharField(max_length=200, null=True)
    activity_level = models.CharField(max_length=200, null=True, choices=ACTIVITY_LEVEL)
    date_created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return" Unknown Customer"

class Progress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    weight = models.FloatField(null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)