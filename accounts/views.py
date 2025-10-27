from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
from .models import *
from .utils import calculate_calories
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect


@login_required(login_url='login')
def home(request):
    customer = None
    calories = None

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = None

        calories = None
        if customer:
            calories = calculate_calories(
                age=customer.age,
                gender=customer.gender.lower(),
                height=customer.height,
                weight=customer.weight,
                activity=customer.activity_level.lower()
            )
        

    return render(request, 'accounts/home.html', {'calories': calories, 'customer':customer} )

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # logs the user in
            return redirect('home')  # redirect to personalized home
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)  # clears the session
    return redirect('login')  # redirect to your login page

def registration(request):
    errors = {}
    
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

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already taken.'

        # Validate email
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered.'

        # Validate password match
        if password != confirm_password:
            errors['password'] = 'Passwords do not match.'

        # If there are errors, re-render template with errors
        if errors:
            return render(request, 'accounts/registration.html', {'errors': errors})

        try:
            height = float(request.POST.get('height', 0))
            weight = float(request.POST.get('weight', 0))
        except ValueError:
            return render(request, 'accounts/registration.html', {'error': 'Invalid height or weight.'})

        age = None
        if birthday_str:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

            # Create a User first
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Then create a linked Customer profile
        customer = Customer.objects.create(
            user=user,
            age=age,
            gender=gender.capitalize(),
            height=height,
            weight=weight,
            activity_level=activity
        )

            
        Progress.objects.create(
            customer=customer,
            weight=weight
        )

        login(request, user)
        return redirect('home')

    return render(request, 'accounts/registration.html')

