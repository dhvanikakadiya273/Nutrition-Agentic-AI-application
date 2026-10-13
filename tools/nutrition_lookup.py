"""
tools/nutrition_lookup.py
Look up nutritional data for a given food item.
Uses a built-in nutrition database; optionally calls the USDA FoodData Central API.
"""

import json
import os
import requests

# ── Built-in fallback database (common foods) ────────────────────────────────────
_NUTRITION_DB: dict = {
    "chicken breast": {
        "per": "100g",
        "calories": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6,
        "fibre_g": 0, "sugar_g": 0, "sodium_mg": 74,
        "vitamins": {"B6": "0.9mg", "B12": "0.3μg", "niacin": "13.7mg"},
    },
    "brown rice": {
        "per": "100g cooked",
        "calories": 112, "protein_g": 2.6, "carbs_g": 23.5, "fat_g": 0.9,
        "fibre_g": 1.8, "sugar_g": 0.4, "sodium_mg": 5,
        "vitamins": {"B1": "0.1mg", "B3": "1.5mg", "manganese": "0.97mg"},
    },
    "egg": {
        "per": "1 large egg (50g)",
        "calories": 72, "protein_g": 6.3, "carbs_g": 0.4, "fat_g": 5,
        "fibre_g": 0, "sugar_g": 0.2, "sodium_mg": 71,
        "vitamins": {"D": "1μg", "B12": "0.6μg", "choline": "147mg"},
    },
    "banana": {
        "per": "1 medium (118g)",
        "calories": 105, "protein_g": 1.3, "carbs_g": 27, "fat_g": 0.4,
        "fibre_g": 3.1, "sugar_g": 14.4, "sodium_mg": 1,
        "vitamins": {"B6": "0.4mg", "C": "10.3mg", "potassium": "422mg"},
    },
    "spinach": {
        "per": "100g raw",
        "calories": 23, "protein_g": 2.9, "carbs_g": 3.6, "fat_g": 0.4,
        "fibre_g": 2.2, "sugar_g": 0.4, "sodium_mg": 79,
        "vitamins": {"K": "483μg", "A": "469μg", "folate": "194μg", "iron": "2.7mg"},
    },
    "salmon": {
        "per": "100g",
        "calories": 208, "protein_g": 20, "carbs_g": 0, "fat_g": 13,
        "fibre_g": 0, "sugar_g": 0, "sodium_mg": 59,
        "vitamins": {"D": "11μg", "B12": "3.2μg", "omega3": "2.3g"},
    },
    "oats": {
        "per": "100g dry",
        "calories": 389, "protein_g": 17, "carbs_g": 66, "fat_g": 7,
        "fibre_g": 10.6, "sugar_g": 1.1, "sodium_mg": 2,
        "vitamins": {"B1": "0.8mg", "iron": "4.7mg", "magnesium": "177mg"},
    },
    "apple": {
        "per": "1 medium (182g)",
        "calories": 95, "protein_g": 0.5, "carbs_g": 25, "fat_g": 0.3,
        "fibre_g": 4.4, "sugar_g": 19, "sodium_mg": 2,
        "vitamins": {"C": "8.4mg", "K": "4μg", "potassium": "195mg"},
    },
    "lentils": {
        "per": "100g cooked",
        "calories": 116, "protein_g": 9, "carbs_g": 20, "fat_g": 0.4,
        "fibre_g": 7.9, "sugar_g": 1.8, "sodium_mg": 2,
        "vitamins": {"folate": "181μg", "iron": "3.3mg", "B1": "0.2mg"},
    },
    "almonds": {
        "per": "28g (about 23 almonds)",
        "calories": 164, "protein_g": 6, "carbs_g": 6, "fat_g": 14,
        "fibre_g": 3.5, "sugar_g": 1.2, "sodium_mg": 0,
        "vitamins": {"E": "7.3mg", "magnesium": "76mg", "calcium": "76mg"},
    },
}


def _usda_lookup(food_query: str) -> dict | None:
    """Try USDA FoodData Central API if an API key is configured."""
    api_key = os.getenv("USDA_API_KEY")
    if not api_key:
        return None
    try:
        url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {"query": food_query, "pageSize": 1, "api_key": api_key}
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        foods = resp.json().get("foods", [])
        if not foods:
            return None
        food = foods[0]
        nutrients = {n["nutrientName"]: n["value"] for n in food.get("foodNutrients", [])}
        return {
            "source": "USDA FoodData Central",
            "description": food.get("description", food_query),
            "per": "100g",
            "calories": nutrients.get("Energy", "N/A"),
            "protein_g": nutrients.get("Protein", "N/A"),
            "carbs_g": nutrients.get("Carbohydrate, by difference", "N/A"),
            "fat_g": nutrients.get("Total lipid (fat)", "N/A"),
            "fibre_g": nutrients.get("Fiber, total dietary", "N/A"),
            "sodium_mg": nutrients.get("Sodium, Na", "N/A"),
        }
    except Exception:
        return None


def lookup_nutrition(food_item: str) -> str:
    """
    Main tool function — called by the agent.
    Returns nutritional information for the requested food item as a formatted string.
    """
    query = food_item.lower().strip()

    # Try USDA API first
    api_result = _usda_lookup(query)
    if api_result:
        return json.dumps(api_result, indent=2)

    # Fall back to local database (fuzzy match)
    for key, data in _NUTRITION_DB.items():
        if key in query or query in key:
            result = {"food": key, **data}
            lines = [
                f"🥗 Nutrition Info — {key.title()} ({data['per']})",
                f"  • Calories   : {data['calories']} kcal",
                f"  • Protein    : {data['protein_g']} g",
                f"  • Carbs      : {data['carbs_g']} g",
                f"  • Fat        : {data['fat_g']} g",
                f"  • Fibre      : {data['fibre_g']} g",
                f"  • Sugar      : {data['sugar_g']} g",
                f"  • Sodium     : {data['sodium_mg']} mg",
                f"  • Key Vitamins/Minerals: {', '.join(f'{k}: {v}' for k, v in data['vitamins'].items())}",
            ]
            return "\n".join(lines)

    return (
        f"No detailed nutrition data found for '{food_item}' in the local database. "
        "Please add a USDA_API_KEY to your .env for broader food lookups. "
        "Generally, common whole foods are: lean meats ~165 kcal/100g, "
        "vegetables ~20-50 kcal/100g, fruits ~50-100 kcal/100g."
    )
