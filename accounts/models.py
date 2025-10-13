from django.db import models

class Customer(models.Model):
    ACTIVITY_LEVEL = (
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active'),
        ('Extra Active', 'Extra Active'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )


    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    goal = models.CharField(max_length=200, null=True)
    activity_level = models.CharField(max_length=200, null=True, choices=ACTIVITY_LEVEL)
    date_created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name

class Progress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    weight = models.FloatField(null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)