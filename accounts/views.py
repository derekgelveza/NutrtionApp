from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .utils import calculate_calories


def home(request):
    calories = None

    if request.method == 'POST':
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender')
        height = float(request.POST.get('height', 0))
        weight = float(request.POST.get('weight', 0))
        activity = request.POST.get('activity')

        print("Form data:", age, gender, height, weight, activity)  # 👈 this line helps debug

        # Make sure all values are present and valid
        if all([age, gender, height, weight, activity]):
            age = int(age)
            height = float(height)
            weight = float(weight)

            calories = calculate_calories(int(age), gender, float(height), float(weight), activity)

            customer = Customer.objects.create(
                age=age,
                gender=gender.capitalize(),
                height=height,
                weight=weight,
                activity_level=activity.capitalize()
                )
            
            Progress.objects.create(
                customer=customer,
                weight=weight
                )

        else:
            print("⚠️ Missing one or more form values!")

    return render(request, 'accounts/home.html', {'calories': calories})

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')


