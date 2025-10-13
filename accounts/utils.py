#calculate calories
def calculate_calories(age, gender, height, weight, activity):
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    activity_multipliers = {
        "sedentary": 1.2,    # Sedentary
        "light": 1.375,  # Lightly active
        "moderate": 1.55,   # Moderately active
        "active": 1.725,  # active
        "very-active": 1.9     # very active
    }
    
    return round(bmr * activity_multipliers.get(activity, 1.2))