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

    GOALS = (
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Weight'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    goal = models.CharField(max_length=200, choices=GOALS, null=True)
    daily_calories = models.FloatField(null=True)

    def __str__(self):
        if self.user:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            return full_name or self.user.username
        return "Unknown Customer"


class NutritionalGoal (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutritional_goals')
    calorie_goal = models.FloatField(null=True)
    carb_ratio = models.FloatField(default=0.4)
    protein_ratio = models.FloatField(default=0.3)
    fat_ratio = models.FloatField(default=3.0)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.calorie_goal} kcal goal"
    

class Meals (models.Model):
    MEAL_TYPES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} ({self.date})"

class Progress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    weight = models.FloatField(null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)