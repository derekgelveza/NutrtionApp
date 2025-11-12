from django import forms
from .models import Meals

class MealForm(forms.ModelForm):
    class Meta:
        model = Meals
        fields = ['meal_type', 'name', 'calories', 'carbs', 'protein', 'fats']
        widgets = {
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control'}),
        }
