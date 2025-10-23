from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
from .models import *
from .utils import calculate_calories


def home(request):
    calories = None

    if request.method == 'POST':
        first_name = str(request.POST.get('first-name', ''))
        last_name = str(request.POST.get('last-name', ''))
        email = str(request.POST.get('email', ''))
        username = str(request.POST.get('username'))
        gender = request.POST.get('gender')
        height = float(request.POST.get('height', 0))
        weight = float(request.POST.get('weight', 0))
        activity = request.POST.get('activity')
        birthday_str = request.POST.get('birthday')

        age = None
        if birthday_str:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


        print("Form data:", first_name, last_name, email, username, age, gender, height, weight, activity, birthday_str, age)  # this line helps debug

        # Make sure all values are present and valid
        if all([age, gender, height, weight, activity]):
            height = float(height)
            weight = float(weight)

            calories = calculate_calories(int(age), gender, float(height), float(weight), activity)

            customer = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
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

def login(request):
    return render(request, 'accounts/login.html')

def registration(request):
    
    if request.method == 'POST':
        first_name = str(request.POST.get('first-name', ''))
        last_name = str(request.POST.get('last-name', ''))
        email = str(request.POST.get('email', ''))
        username = str(request.POST.get('username', ''))
        password = str(request.POST.get('password', ''))
        confirm_password = str(request.POST.get('confirm-password', ''))
        birthday_str = request.POST.get('birthday', '')
        gender = request.POST.get('gender')
        height = float(request.POST.get('height', 0))
        weight = float(request.POST.get('weight', 0))
        activity = request.POST.get('activity')

        age = None
        if birthday_str:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

            print("Form data:", first_name, last_name, email, username, password, confirm_password, age, gender, height, weight, activity, birthday_str, age)



    return render(request, 'accounts/registration.html')

