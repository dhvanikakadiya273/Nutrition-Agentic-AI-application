"""
tools/calorie_calculator.py
Calculate Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE).
Uses the Mifflin-St Jeor equation — the most accurate for general populations.
"""

import json


_ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,           # Little or no exercise
    "lightly_active": 1.375,    # Light exercise 1–3 days/week
    "moderately_active": 1.55,  # Moderate exercise 3–5 days/week
    "very_active": 1.725,       # Hard exercise 6–7 days/week
    "extra_active": 1.9,        # Very hard exercise / physical job
}

_ACTIVITY_ALIASES = {
    "sedentary": "sedentary",
    "light": "lightly_active",
    "lightly active": "lightly_active",
    "lightly_active": "lightly_active",
    "moderate": "moderately_active",
    "moderately active": "moderately_active",
    "moderately_active": "moderately_active",
    "active": "very_active",
    "very active": "very_active",
    "very_active": "very_active",
    "extra active": "extra_active",
    "extra_active": "extra_active",
    "athlete": "extra_active",
}


def calculate_calories(input_str: str) -> str:
    """
    Main tool function — called by the agent.
    input_str: JSON string with keys:
      - weight_kg  : float  (e.g. 70)
      - height_cm  : float  (e.g. 175)
      - age        : int    (e.g. 28)
      - gender     : str    ("male" | "female")
      - activity_level: str (see _ACTIVITY_ALIASES keys)
    """
    try:
        params = json.loads(input_str)
    except (json.JSONDecodeError, TypeError):
        return (
            "Could not parse input. Please provide a JSON string like: "
            '{"weight_kg": 70, "height_cm": 175, "age": 28, "gender": "male", "activity_level": "moderately_active"}'
        )

    try:
        weight = float(params["weight_kg"])
        height = float(params["height_cm"])
        age = int(params["age"])
        gender = str(params.get("gender", "male")).lower().strip()
        activity_raw = str(params.get("activity_level", "moderately_active")).lower().strip()
    except (KeyError, ValueError) as exc:
        return f"Missing or invalid parameter: {exc}. Please supply weight_kg, height_cm, age, gender, and activity_level."

    # ── Mifflin-St Jeor BMR ──────────────────────────────────────────────────────
    if gender in ("male", "m", "man"):
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        gender_label = "Male"
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        gender_label = "Female"

    activity_key = _ACTIVITY_ALIASES.get(activity_raw, "moderately_active")
    multiplier = _ACTIVITY_MULTIPLIERS[activity_key]
    tdee = bmr * multiplier

    # ── Goal recommendations ─────────────────────────────────────────────────────
    weight_loss = tdee - 500          # ~0.5 kg/week loss
    aggressive_loss = tdee - 750      # ~0.75 kg/week loss
    weight_gain = tdee + 300          # lean bulk
    muscle_gain = tdee + 500          # standard bulk

    activity_label = activity_key.replace("_", " ").title()

    lines = [
        "🏋️  Daily Calorie & Macronutrient Report",
        "=" * 50,
        f"  Gender          : {gender_label}",
        f"  Weight          : {weight} kg",
        f"  Height          : {height} cm",
        f"  Age             : {age} years",
        f"  Activity Level  : {activity_label}",
        "",
        f"  📊 BMR (at rest)  : {bmr:.0f} kcal/day",
        f"  🔥 TDEE (maintain): {tdee:.0f} kcal/day",
        "",
        "  🎯 Goal-Based Calorie Targets:",
        f"    • Maintain weight       → {tdee:.0f} kcal",
        f"    • Mild weight loss      → {weight_loss:.0f} kcal  (−500/day ≈ 0.5 kg/week)",
        f"    • Aggressive weight loss→ {aggressive_loss:.0f} kcal  (−750/day ≈ 0.75 kg/week)",
        f"    • Lean muscle gain      → {weight_gain:.0f} kcal  (+300/day)",
        f"    • Standard bulk         → {muscle_gain:.0f} kcal  (+500/day)",
        "",
        "  🥦 Recommended Macro Split (for maintenance):",
        f"    • Protein  30% → {tdee * 0.30 / 4:.0f} g/day",
        f"    • Carbs    40% → {tdee * 0.40 / 4:.0f} g/day",
        f"    • Fat      30% → {tdee * 0.30 / 9:.0f} g/day",
        "",
        "=" * 50,
        "⚠️  These are estimates using the Mifflin-St Jeor equation.",
        "   Consult a healthcare professional for personalised advice.",
    ]

    return "\n".join(lines)
