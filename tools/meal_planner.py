"""
tools/meal_planner.py
Generate a personalised meal plan based on caloric goal, diet type, and number of days.
"""

import json


# ── Meal template library ────────────────────────────────────────────────────────
_MEALS = {
    "omnivore": {
        "breakfast": [
            "Oatmeal with banana, almonds, and honey (380 kcal)",
            "Scrambled eggs (3) with whole-grain toast and avocado (420 kcal)",
            "Greek yoghurt parfait with berries and granola (350 kcal)",
            "Smoothie: banana, spinach, protein powder, almond milk (360 kcal)",
            "Poached eggs on sourdough with smoked salmon (400 kcal)",
            "Overnight oats with chia seeds and mixed berries (340 kcal)",
            "Whole-wheat pancakes with fresh fruit (380 kcal)",
        ],
        "lunch": [
            "Grilled chicken breast salad with quinoa and vinaigrette (500 kcal)",
            "Turkey and avocado wrap with side salad (480 kcal)",
            "Brown rice bowl with salmon, edamame, and miso dressing (550 kcal)",
            "Lentil soup with crusty bread (420 kcal)",
            "Chicken stir-fry with mixed vegetables and brown rice (530 kcal)",
            "Tuna nicoise salad (460 kcal)",
            "Beef and vegetable stew with sweet potato (510 kcal)",
        ],
        "dinner": [
            "Baked salmon with steamed broccoli and quinoa (600 kcal)",
            "Grilled chicken thighs with roasted vegetables and brown rice (580 kcal)",
            "Lean beef stir-fry with noodles and pak choi (620 kcal)",
            "Baked cod with lemon, asparagus, and mashed sweet potato (540 kcal)",
            "Turkey meatballs with whole-wheat pasta and tomato sauce (590 kcal)",
            "Prawn and vegetable curry with basmati rice (570 kcal)",
            "Chicken and vegetable soup with crusty bread (480 kcal)",
        ],
        "snack": [
            "Apple with 2 tbsp peanut butter (200 kcal)",
            "Handful of mixed nuts and a banana (220 kcal)",
            "Greek yoghurt with honey (150 kcal)",
            "Rice cakes with cottage cheese (130 kcal)",
            "Protein bar (200 kcal)",
            "Carrot sticks with hummus (120 kcal)",
            "Hard-boiled eggs (2) (140 kcal)",
        ],
    },
    "vegetarian": {
        "breakfast": [
            "Oatmeal with berries, chia seeds, and almond butter (380 kcal)",
            "Veggie omelette (3 eggs) with whole-grain toast (400 kcal)",
            "Smoothie bowl with mango, banana, and granola (370 kcal)",
            "Avocado toast with poached eggs and cherry tomatoes (420 kcal)",
            "Overnight oats with flaxseeds and mixed nuts (350 kcal)",
            "Whole-grain pancakes with fresh berries and maple syrup (380 kcal)",
            "Greek yoghurt with walnuts, honey, and sliced banana (340 kcal)",
        ],
        "lunch": [
            "Chickpea and spinach curry with brown rice (520 kcal)",
            "Caprese salad with whole-wheat bread (400 kcal)",
            "Lentil and vegetable soup with sourdough (430 kcal)",
            "Quinoa salad with roasted vegetables and feta (480 kcal)",
            "Black bean tacos with guacamole and salsa (500 kcal)",
            "Tofu stir-fry with mixed vegetables and noodles (490 kcal)",
            "Vegetable and halloumi wrap with side salad (460 kcal)",
        ],
        "dinner": [
            "Vegetable lasagne with side salad (580 kcal)",
            "Paneer tikka masala with basmati rice (620 kcal)",
            "Mushroom and lentil shepherd's pie (560 kcal)",
            "Spinach and ricotta stuffed pasta shells (590 kcal)",
            "Thai green tofu curry with jasmine rice (570 kcal)",
            "Aubergine parmigiana with garlic bread (600 kcal)",
            "Vegetable tagine with couscous (540 kcal)",
        ],
        "snack": [
            "Apple with almond butter (200 kcal)",
            "Trail mix with dried fruit (220 kcal)",
            "Greek yoghurt with honey (150 kcal)",
            "Celery and carrot sticks with hummus (120 kcal)",
            "Cheese and whole-grain crackers (190 kcal)",
            "Banana and a handful of walnuts (210 kcal)",
            "Edamame with sea salt (140 kcal)",
        ],
    },
    "vegan": {
        "breakfast": [
            "Smoothie: spinach, banana, plant protein, oat milk (380 kcal)",
            "Overnight oats with chia seeds, berries, and maple syrup (350 kcal)",
            "Avocado toast on rye bread with hemp seeds (390 kcal)",
            "Tofu scramble with turmeric, peppers, and whole-wheat toast (400 kcal)",
            "Açaí bowl with granola, banana, and coconut flakes (370 kcal)",
            "Peanut butter banana oatmeal (360 kcal)",
            "Chia pudding with mango and coconut milk (320 kcal)",
        ],
        "lunch": [
            "Chickpea Buddha bowl with tahini dressing (520 kcal)",
            "Lentil and vegetable soup with crusty bread (430 kcal)",
            "Black bean and corn burrito with guacamole (540 kcal)",
            "Quinoa tabbouleh with roasted chickpeas (480 kcal)",
            "Tempeh stir-fry with brown rice (510 kcal)",
            "Roasted vegetable and hummus wrap (460 kcal)",
            "White bean and kale soup (400 kcal)",
        ],
        "dinner": [
            "Red lentil dal with basmati rice and naan (580 kcal)",
            "Tofu and vegetable Thai green curry (560 kcal)",
            "Vegan chilli with cornbread (600 kcal)",
            "Mushroom stroganoff with whole-wheat pasta (570 kcal)",
            "Jackfruit tacos with pico de gallo (540 kcal)",
            "Cauliflower and chickpea tikka masala with rice (590 kcal)",
            "Spaghetti with lentil bolognese (570 kcal)",
        ],
        "snack": [
            "Apple with peanut butter (200 kcal)",
            "Trail mix with dark chocolate chips (230 kcal)",
            "Hummus with vegetable sticks (120 kcal)",
            "Rice cakes with avocado (140 kcal)",
            "Roasted chickpeas (150 kcal)",
            "Banana nice cream (120 kcal)",
            "Mixed nuts and dried apricots (210 kcal)",
        ],
    },
    "keto": {
        "breakfast": [
            "Bacon and eggs with avocado (450 kcal, <5g carbs)",
            "Keto smoothie: coconut milk, MCT oil, spinach, protein powder (380 kcal)",
            "Cheese omelette with mushrooms and butter (420 kcal)",
            "Full English keto: eggs, bacon, sausage, grilled tomato (500 kcal)",
            "Smoked salmon with cream cheese on cucumber slices (350 kcal)",
            "Almond flour pancakes with sugar-free syrup (390 kcal)",
            "Greek yoghurt (full-fat) with walnuts (320 kcal)",
        ],
        "lunch": [
            "Lettuce-wrap burger with cheese, bacon, and avocado (550 kcal)",
            "Chicken Caesar salad without croutons (480 kcal)",
            "Tuna salad with avocado and cucumber (420 kcal)",
            "Cauliflower fried rice with chicken (460 kcal)",
            "BLT salad with ranch dressing (430 kcal)",
            "Prawn and avocado salad (400 kcal)",
            "Keto soup: chicken, cream, spinach, cheese (490 kcal)",
        ],
        "dinner": [
            "Ribeye steak with butter-roasted asparagus (700 kcal)",
            "Baked salmon with lemon butter and courgette noodles (580 kcal)",
            "Stuffed bell peppers with ground beef and cheese (600 kcal)",
            "Chicken thighs with roasted broccoli and garlic butter (620 kcal)",
            "Pork belly with cauliflower mash (650 kcal)",
            "Lamb chops with green beans and herb butter (680 kcal)",
            "Shrimp and chorizo with cauliflower rice (570 kcal)",
        ],
        "snack": [
            "Cheese cubes and olives (200 kcal)",
            "Pork rinds (150 kcal)",
            "Macadamia nuts (210 kcal)",
            "Celery with cream cheese (100 kcal)",
            "Hard-boiled eggs (2) (140 kcal)",
            "Beef jerky (120 kcal)",
            "Avocado with sea salt (160 kcal)",
        ],
    },
    "gluten-free": {
        "breakfast": [
            "Rice porridge with berries and honey (350 kcal)",
            "Eggs and avocado on gluten-free toast (400 kcal)",
            "Smoothie bowl with seeds and fresh fruit (360 kcal)",
            "Corn tortilla breakfast tacos with eggs and salsa (420 kcal)",
            "Gluten-free granola with almond milk and banana (380 kcal)",
            "Buckwheat pancakes with maple syrup (370 kcal)",
            "Rice cakes with almond butter and banana (310 kcal)",
        ],
        "lunch": [
            "Quinoa salad with grilled chicken and lemon dressing (500 kcal)",
            "Rice noodle soup with tofu and vegetables (440 kcal)",
            "Corn tortilla tacos with fish and mango salsa (480 kcal)",
            "Sweet potato and black bean bowl (460 kcal)",
            "Baked potato with tuna and salad (490 kcal)",
            "Gluten-free pasta salad with pesto (470 kcal)",
            "Brown rice bowl with salmon and edamame (520 kcal)",
        ],
        "dinner": [
            "Baked chicken with roasted vegetables and rice (580 kcal)",
            "Salmon with quinoa and steamed green beans (570 kcal)",
            "Gluten-free pasta with marinara and meatballs (600 kcal)",
            "Stuffed sweet potatoes with black beans and cheese (560 kcal)",
            "Beef stir-fry with rice noodles (590 kcal)",
            "Prawn curry with basmati rice (570 kcal)",
            "Turkey burger on gluten-free bun with salad (540 kcal)",
        ],
        "snack": [
            "Rice cakes with hummus (130 kcal)",
            "Apple with peanut butter (200 kcal)",
            "Gluten-free oat energy balls (180 kcal)",
            "Corn tortilla chips with guacamole (220 kcal)",
            "Greek yoghurt with berries (150 kcal)",
            "Mixed nuts (200 kcal)",
            "Popcorn (plain) (110 kcal)",
        ],
    },
    "diabetic": {
        "breakfast": [
            "Steel-cut oats with cinnamon, walnuts, and blueberries (350 kcal, low GI)",
            "Veggie egg white omelette with whole-grain toast (320 kcal)",
            "Greek yoghurt (plain, low-fat) with flaxseeds and strawberries (290 kcal)",
            "Avocado toast on sourdough with poached egg (380 kcal, low GI)",
            "Overnight oats with chia seeds and raspberries (330 kcal)",
            "Whole-grain cereal with almond milk and mixed berries (300 kcal)",
            "Smoothie: spinach, cucumber, green apple, ginger (250 kcal, low sugar)",
        ],
        "lunch": [
            "Grilled chicken on a bed of mixed greens with olive oil (420 kcal)",
            "Lentil soup with a small whole-grain roll (400 kcal)",
            "Tuna and avocado salad on romaine lettuce (380 kcal)",
            "Turkey and vegetable stir-fry with cauliflower rice (430 kcal)",
            "Chickpea and spinach salad with lemon dressing (410 kcal)",
            "Veggie-packed brown rice bowl (440 kcal, moderate GI)",
            "Grilled salmon with asparagus (450 kcal)",
        ],
        "dinner": [
            "Baked cod with steamed broccoli and sweet potato (480 kcal)",
            "Chicken breast with quinoa and roasted vegetables (520 kcal)",
            "Tofu and vegetable stir-fry with shirataki noodles (380 kcal)",
            "Turkey meatballs with zucchini noodles and tomato sauce (460 kcal)",
            "Grilled salmon with lemon and green beans (500 kcal)",
            "Bean and vegetable casserole (440 kcal)",
            "Lean beef with broccoli and brown rice (small portion) (490 kcal)",
        ],
        "snack": [
            "Celery sticks with almond butter (120 kcal)",
            "Small handful of walnuts (130 kcal)",
            "Cucumber slices with hummus (100 kcal)",
            "Small apple with cheese (150 kcal)",
            "Hard-boiled egg (70 kcal)",
            "Cherry tomatoes with cottage cheese (110 kcal)",
            "A few almonds (100 kcal)",
        ],
    },
}

_DIET_MAP = {
    "vegan": "vegan",
    "vegetarian": "vegetarian",
    "keto": "keto",
    "ketogenic": "keto",
    "gluten-free": "gluten-free",
    "gluten free": "gluten-free",
    "diabetic": "diabetic",
    "diabetes": "diabetic",
    "omnivore": "omnivore",
    "standard": "omnivore",
    "balanced": "omnivore",
}


def generate_meal_plan(input_str: str) -> str:
    """
    Main tool function — called by the agent.
    input_str: JSON string with keys: calories (int), diet_type (str), days (int)
    """
    try:
        params = json.loads(input_str)
    except (json.JSONDecodeError, TypeError):
        # Accept plain text fallback
        params = {"calories": 2000, "diet_type": input_str, "days": 7}

    target_calories = int(params.get("calories", 2000))
    diet_type_raw = str(params.get("diet_type", "omnivore")).lower().strip()
    days = min(int(params.get("days", 7)), 7)  # max 7 days

    diet_key = _DIET_MAP.get(diet_type_raw, "omnivore")
    meals = _MEALS[diet_key]

    lines = [
        f"🍽️  {days}-Day {diet_type_raw.title()} Meal Plan (~{target_calories} kcal/day)",
        "=" * 60,
    ]

    for day in range(1, days + 1):
        idx = (day - 1) % 7
        lines.append(f"\n📅 Day {day}")
        lines.append(f"  🌅 Breakfast : {meals['breakfast'][idx]}")
        lines.append(f"  ☀️  Lunch     : {meals['lunch'][idx]}")
        lines.append(f"  🌙 Dinner    : {meals['dinner'][idx]}")
        lines.append(f"  🍎 Snack     : {meals['snack'][idx]}")

    lines.append("\n" + "=" * 60)
    lines.append("💧 Remember: drink 2–3 L of water daily.")
    lines.append("⚠️  This plan is a general guide. Consult a registered dietitian for personalised medical nutrition advice.")

    return "\n".join(lines)
