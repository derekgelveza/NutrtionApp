from django.shortcuts import render
import json
import openai
from django.http import HttpResponse
from datetime import datetime, date
from .forms import MealForm
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
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods



@login_required(login_url='login')
def dashboard_data(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('setup')

    if not customer.daily_calories:
        return JsonResponse({'error': 'Daily calories not set'}, status=400)


    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    meals = Meals.objects.filter(user=request.user, date=selected_date)

    eaten_calories = sum(meal.calories for meal in meals)
    eaten_protein = sum(meal.protein for meal in meals)
    eaten_carbs = sum(meal.carbs for meal in meals)
    eaten_fats = sum(meal.fats for meal in meals)

    daily_calories = round(customer.daily_calories)
    protein_goal = round(daily_calories * 0.3 / 4)
    carbs_goal   = round(daily_calories * 0.4 / 4)
    fats_goal    = round(daily_calories * 0.3 / 9)

    return JsonResponse({
        "daily_calories": daily_calories,
        "eaten_calories": eaten_calories,
        "remaining_calories": daily_calories - eaten_calories,

        "protein_goal": protein_goal,
        "carbs_goal": carbs_goal,
        "fats_goal": fats_goal,

        "protein_total": eaten_protein,
        "carbs_total": eaten_carbs,
        "fats_total": eaten_fats,

        "protein_remaining": protein_goal - eaten_protein,
        "carbs_remaining": carbs_goal - eaten_carbs,
        "fats_remaining": fats_goal - eaten_fats,


        "meals": [
            {
                "id": meal.id,
                "name": meal.name,
                "calories": meal.calories,
                "protein": meal.protein,
                "carbs": meal.carbs,
                "fats": meal.fats,
                "meal_type": meal.meal_type,
            }
            for meal in meals
        ]
    })

@login_required
@require_POST
def add_meal(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "errors": {"__all__": ["Invalid JSON"]}}, status=400)

    required_fields = ['name', 'calories', 'protein', 'carbs', 'fats', 'meal_type', 'date']
    errors = {}

    for field in required_fields:
        if field not in data or data[field] in [None, '']:
            errors[field] = ['This field is required.']

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    try:
        calories = float(data['calories'])
        protein = float(data['protein'])
        carbs = float(data['carbs'])
        fats = float(data['fats'])
        selected_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError as e:
        return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}}, status=400)

    meal = Meals.objects.create(
        user=request.user,
        meal_type=data['meal_type'],
        name=data['name'],
        calories=calories,
        protein=protein,
        carbs=carbs,
        fats=fats,
        date=selected_date
    )

    return JsonResponse({"success": True, "id": meal.id})

@login_required
@require_POST
def edit_meal(request, id):
    meal = get_object_or_404(Meals, id=id, user=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "errors": {"__all__": ["Invalid JSON"]}}, status=400)

    required_fields = ['name', 'calories', 'protein', 'carbs', 'fats', 'meal_type', 'date']
    errors = {}
    for field in required_fields:
        if field not in data or data[field] in [None, '']:
            errors[field] = ['This field is required.']
    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    try:
        meal.calories = float(data['calories'])
        meal.protein = float(data['protein'])
        meal.carbs = float(data['carbs'])
        meal.fats = float(data['fats'])
        meal.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError as e:
        return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}}, status=400)

    meal.name = data['name']
    meal.meal_type = data['meal_type']
    meal.save()

    return JsonResponse({"success": True})


@login_required
@require_http_methods(["DELETE"])
def delete_meal(request, id):
    meal = get_object_or_404(Meals, id=id, user=request.user)
    meal.delete()
    return JsonResponse({"success": True})



@login_required(login_url='login')
def dashboard(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('setup')
    
    calories = round(customer.daily_calories) if customer.daily_calories else 0

    form = MealForm()

    return render(request, 'accounts/dashboard.html', {'calories': calories, 'customer': customer, 'form': form})


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
    logout(request) 
    return redirect('login')

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


@login_required(login_url='login')
def fridgeAi(request):
    
    return render(request, 'accounts/fridgeAi.html')




#AI

@login_required
def meal_ideas(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        ingredients = data.get('ingredients', [])
        if not ingredients:
            return JsonResponse({'success': False, 'error': 'No ingredients provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    ingredients_str = ', '.join(ingredients)

    prompt = f"""
    Suggest 3 healthy meals using the following ingredients: {ingredients_str}.
    For each meal, give:
    - Name
    - Estimated calories
    - Protein (g)
    - Carbs (g)
    - Fats (g)
    Return in JSON like:
    [
      {{ "name": "Meal 1", "calories": 400, "protein": 30, "carbs": 40, "fats": 10 }},
      ...
    ]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        text_response = response['choices'][0]['message']['content']

        import ast
        try:
            meals = json.loads(text_response)
        except json.JSONDecodeError:
            meals = ast.literal_eval(text_response)

        return JsonResponse({'success': True, 'meals': meals})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
