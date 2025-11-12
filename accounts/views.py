from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
from .models import *
from .utils import calculate_calories, adjust_calories_for_goal
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect


@login_required(login_url='login')
def dashboard_data(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('setup')

    if not customer.daily_calories:
        return JsonResponse({'error': 'Daily calories not set'}, status=400)
    
    meals = Meals.objects.filter(user=request.user, date=date.today())
    eaten_calories = sum(meal.calories for meal in meals)
    remaining_calories = customer.daily_calories - eaten_calories

    data = {
        'daily_calories': round(customer.daily_calories),
        'eaten_calories': round(eaten_calories),
        'remaining_calories': round(remaining_calories),
        'carbs': round(customer.daily_calories * 0.4) / 4,
        "protein": round(customer.daily_calories * 0.3) / 4,
        'fats': round(customer.daily_calories * 0.3) / 9
    }
        
    return JsonResponse(data)

@login_required(login_url='login')
def dashboard(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('setup')
    
    calories = round(customer.daily_calories) if customer.daily_calories else 0

    return render(request, 'accounts/dashboard.html', {'calories': calories, 'customer': customer})


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
            return redirect('dashboard')  # redirect to personalized home
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
        
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already taken.'

        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered.'

        if password != confirm_password:
            errors['password'] = 'Passwords do not match.'

        if errors:
            return render(request, 'accounts/registration.html', {'errors': errors})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)
        return redirect('setup')

    return render(request, 'accounts/registration.html')

@login_required(login_url='login')
@csrf_protect
def user_setup(request):
    errors = {}

    if request.method == 'POST':
        birthday_str = request.POST.get('birthday', '')
        gender = request.POST.get('gender')
        activity = request.POST.get('activity')
        goal = request.POST.get('goal')

        if not birthday_str:
            errors['birthday'] = 'Birthday is required.'
        if not gender:
            errors['gender'] = 'Gender is required.'
        if not activity:
            errors['activity'] = 'Activity level is required.'
        if not goal:
            errors['goal'] = 'Goal is required.'

        try:
            height = float(request.POST.get('height', 0))
            weight = float(request.POST.get('weight', 0))
            if height <= 0 or weight <= 0:
                errors['invalid'] = 'Height and weight must be greater than 0.'
        except ValueError:
            errors['invalid'] = 'Invalid height or weight.'

        if errors:
            return render(request, 'accounts/setup.html', {'errors': errors})

        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        # Calculate calories
        base_calories = calculate_calories(age, gender.lower(), height, weight, activity.lower())
        final_calories = adjust_calories_for_goal(base_calories, goal.lower())

        # Create or update Customer profile
        customer, created = Customer.objects.update_or_create(
            user=request.user,
            defaults={
                'age': age,
                'gender': gender.capitalize(),
                'height': height,
                'weight': weight,
                'activity_level': activity,
                'goal': goal,
                'daily_calories': final_calories
            }
        )

        # Create a Progress entry for the first weight if it’s new
        if created or (customer.weight != weight):
            Progress.objects.create(customer=customer, weight=weight)

        # Redirect to dashboard or home
        return redirect('dashboard')
    return render(request, 'accounts/setup.html')

