"""Quick smoke-test for all three agent tools (no emoji output)."""
import json, sys

sys.stdout.reconfigure(encoding="utf-8")

from tools.nutrition_lookup import lookup_nutrition
from tools.meal_planner import generate_meal_plan
from tools.calorie_calculator import calculate_calories

print("=== NutritionLookup ===")
print(lookup_nutrition("chicken breast"))

print("\n=== CalorieCalculator ===")
print(calculate_calories(json.dumps({
    "weight_kg": 70, "height_cm": 175, "age": 28,
    "gender": "male", "activity_level": "moderately_active"
})))

print("\n=== MealPlanner ===")
print(generate_meal_plan(json.dumps({
    "calories": 1800, "diet_type": "vegetarian", "days": 3
})))

print("\nAll tools working correctly!")
