"""
🍕 Pizza Party Order App
A simple Flask app for ordering pizzas at a party!
"""

import json
import os
import re
import secrets
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# File paths
ORDERS_FILE = "orders.json"
TOKENS_FILE = "tokens.json"
INGREDIENTS_FILE = "ingredients.json"
TRANSLATIONS_FILE = "translations.json"

# Static list of categories in display order
CATEGORIES = ["bases", "cheeses", "meats", "veggies", "extras"]

# Fixed list of available emojis for ingredients
AVAILABLE_EMOJIS = [
    "🍅", "🧀", "🥛", "🔥", "🌿", "🐐", "🍖", "🐷", "🥓", "🌭", "🍗",
    "🍄", "🧅", "🫑", "🫒", "🥬", "🌶️", "🍍", "🥗", "🧄", "🌱", "✨",
    "🥚", "🐟", "🦐", "🥩", "🌽", "🥒", "🍆", "🥦", "🍋", "🥜", "🍯",
    "🫛", "🥕", "🍇", "🥑", "🌰", "🧈", "🥫", "🍳", "❤️", "⭐", "🔶"
]

# Default ingredients (used on first run)
# Each ingredient has name_en and name_sk for multilingual support
DEFAULT_INGREDIENTS = {
    "bases": [
        {"id": "tomato", "name_en": "Tomato Sauce", "name_sk": "Paradajkový základ", "emoji": "🍅", "enabled": True},
        {"id": "white", "name_en": "White/Cream Sauce", "name_sk": "Smotanový základ", "emoji": "🥛", "enabled": True},
        {"id": "bbq", "name_en": "BBQ Sauce", "name_sk": "BBQ omáčka", "emoji": "🔥", "enabled": True},
        {"id": "pesto", "name_en": "Pesto", "name_sk": "Pesto", "emoji": "🌿", "enabled": True},
    ],
    "cheeses": [
        {"id": "mozzarella", "name_en": "Mozzarella", "name_sk": "Mozzarella", "emoji": "🧀", "enabled": True},
        {"id": "parmesan", "name_en": "Parmesan", "name_sk": "Parmezán", "emoji": "🧀", "enabled": True},
        {"id": "gorgonzola", "name_en": "Gorgonzola", "name_sk": "Gorgonzola", "emoji": "🧀", "enabled": True},
        {"id": "goat", "name_en": "Goat Cheese", "name_sk": "Kozí syr", "emoji": "🐐", "enabled": True},
    ],
    "meats": [
        {"id": "pepperoni", "name_en": "Pepperoni", "name_sk": "Pepperoni", "emoji": "🍖", "enabled": True},
        {"id": "ham", "name_en": "Ham", "name_sk": "Šunka", "emoji": "🐷", "enabled": True},
        {"id": "bacon", "name_en": "Bacon", "name_sk": "Slanina", "emoji": "🥓", "enabled": True},
        {"id": "sausage", "name_en": "Italian Sausage", "name_sk": "Talianská klobása", "emoji": "🌭", "enabled": True},
        {"id": "chicken", "name_en": "Chicken", "name_sk": "Kura", "emoji": "🍗", "enabled": True},
    ],
    "veggies": [
        {"id": "mushrooms", "name_en": "Mushrooms", "name_sk": "Huby", "emoji": "🍄", "enabled": True},
        {"id": "onions", "name_en": "Onions", "name_sk": "Cibuľa", "emoji": "🧅", "enabled": True},
        {"id": "peppers", "name_en": "Bell Peppers", "name_sk": "Papriky", "emoji": "🫑", "enabled": True},
        {"id": "olives", "name_en": "Olives", "name_sk": "Olivy", "emoji": "🫒", "enabled": True},
        {"id": "tomatoes", "name_en": "Fresh Tomatoes", "name_sk": "Čerstvé paradajky", "emoji": "🍅", "enabled": True},
        {"id": "spinach", "name_en": "Spinach", "name_sk": "Špenát", "emoji": "🥬", "enabled": True},
        {"id": "jalapenos", "name_en": "Jalapeños", "name_sk": "Jalapeños", "emoji": "🌶️", "enabled": True},
        {"id": "pineapple", "name_en": "Pineapple", "name_sk": "Ananás", "emoji": "🍍", "enabled": True},
        {"id": "arugula", "name_en": "Arugula", "name_sk": "Rukola", "emoji": "🥗", "enabled": True},
    ],
    "extras": [
        {"id": "garlic", "name_en": "Extra Garlic", "name_sk": "Extra cesnak", "emoji": "🧄", "enabled": True},
        {"id": "basil", "name_en": "Fresh Basil", "name_sk": "Čerstvá bazalka", "emoji": "🌿", "enabled": True},
        {"id": "oregano", "name_en": "Oregano", "name_sk": "Oregano", "emoji": "🌱", "enabled": True},
        {"id": "chili", "name_en": "Chili Flakes", "name_sk": "Chilli vločky", "emoji": "🌶️", "enabled": True},
        {"id": "truffle", "name_en": "Truffle Oil", "name_sk": "Hľuzovkový olej", "emoji": "✨", "enabled": True},
    ]
}


def load_tokens():
    """Load or generate access tokens."""
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r") as f:
            return json.load(f)
    else:
        tokens = {
            "party": secrets.token_urlsafe(16),
            "admin": secrets.token_urlsafe(16)
        }
        with open(TOKENS_FILE, "w") as f:
            json.dump(tokens, f, indent=2)
        print("\n" + "="*50)
        print("🍕 PIZZA PARTY TOKENS GENERATED!")
        print("="*50)
        print(f"📋 Party Link: http://localhost:5000/party/{tokens['party']}")
        print(f"👑 Admin Link: http://localhost:5000/admin/{tokens['admin']}")
        print("="*50 + "\n")
        return tokens


def load_translations():
    """Load translations from file."""
    if os.path.exists(TRANSLATIONS_FILE):
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"en": {}, "sk": {}}


def load_ingredients():
    """Load ingredients from file or create default."""
    if os.path.exists(INGREDIENTS_FILE):
        with open(INGREDIENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_ingredients(DEFAULT_INGREDIENTS)
        return DEFAULT_INGREDIENTS


def save_ingredients(ingredients):
    """Save ingredients to file."""
    with open(INGREDIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, indent=2, ensure_ascii=False)


def get_enabled_ingredients():
    """Get only enabled ingredients for the party page."""
    all_ingredients = load_ingredients()
    enabled = {}
    for category in CATEGORIES:
        items = all_ingredients.get(category, [])
        enabled[category] = [item for item in items if item.get("enabled", True)]
    return enabled


def load_orders():
    """Load orders from JSON file."""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_orders(orders):
    """Save orders to JSON file."""
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)


TOKENS = load_tokens()


@app.route("/")
def home():
    """Redirect to nowhere - need token to access."""
    return "🍕 Pizza Party! You need a valid link to join.", 403


@app.route("/party/<token>")
def party(token):
    """Main party page - order your pizza!"""
    if token != TOKENS["party"]:
        return "🚫 Invalid party link!", 403
    ingredients = get_enabled_ingredients()
    translations = load_translations()
    return render_template(
        "index.html", 
        token=token, 
        ingredients=ingredients,
        categories=CATEGORIES,
        translations=translations
    )


@app.route("/admin/<token>")
def admin(token):
    """Admin page - see all orders and manage ingredients."""
    if token != TOKENS["admin"]:
        return "🚫 Invalid admin link!", 403
    orders = load_orders()
    ingredients = load_ingredients()
    translations = load_translations()
    return render_template(
        "admin.html", 
        orders=orders, 
        ingredients=ingredients,
        categories=CATEGORIES,
        available_emojis=AVAILABLE_EMOJIS,
        translations=translations
    )


# ============ ORDER APIs ============

@app.route("/api/order/<token>", methods=["GET"])
def get_order(token):
    """Get order for a specific person."""
    if token != TOKENS["party"]:
        return jsonify({"error": "Invalid token"}), 403
    
    name = request.args.get("name", "").strip().lower()
    if not name:
        return jsonify({"error": "Name required"}), 400
    
    orders = load_orders()
    order = orders.get(name, None)
    return jsonify({"order": order})


@app.route("/api/order/<token>", methods=["POST"])
def save_order(token):
    """Save/update an order."""
    if token != TOKENS["party"]:
        return jsonify({"error": "Invalid token"}), 403
    
    data = request.json
    name = data.get("name", "").strip().lower()
    ingredients = data.get("ingredients", {})
    cutting = data.get("cutting", 8)  # Default to 8 slices
    
    if not name:
        return jsonify({"error": "Name required"}), 400
    
    orders = load_orders()
    
    # Preserve done status if it exists
    existing_done = orders.get(name, {}).get("done", False)
    
    orders[name] = {
        "display_name": data.get("name", "").strip(),
        "ingredients": ingredients,
        "cutting": cutting,
        "done": existing_done
    }
    save_orders(orders)
    
    return jsonify({"success": True, "message": "Pizza order saved! 🍕"})


@app.route("/api/orders/<token>", methods=["GET"])
def get_all_orders(token):
    """Get all orders (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    orders = load_orders()
    return jsonify({"orders": orders})


@app.route("/api/order/<token>/<name>", methods=["DELETE"])
def delete_order(token, name):
    """Delete an order (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    orders = load_orders()
    name_lower = name.lower()
    if name_lower in orders:
        del orders[name_lower]
        save_orders(orders)
        return jsonify({"success": True})
    return jsonify({"error": "Order not found"}), 404


@app.route("/api/order/<token>/<name>/done", methods=["PUT"])
def toggle_order_done(token, name):
    """Toggle done status of an order (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    data = request.json
    done = data.get("done", False)
    
    orders = load_orders()
    name_lower = name.lower()
    
    if name_lower in orders:
        orders[name_lower]["done"] = done
        save_orders(orders)
        return jsonify({"success": True, "done": done})
    
    return jsonify({"error": "Order not found"}), 404


# ============ INGREDIENT MANAGEMENT APIs (Admin only) ============

@app.route("/api/ingredients/<token>", methods=["GET"])
def get_ingredients(token):
    """Get all ingredients (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    ingredients = load_ingredients()
    return jsonify({"ingredients": ingredients, "categories": CATEGORIES, "emojis": AVAILABLE_EMOJIS})


@app.route("/api/ingredients/<token>/<category>", methods=["POST"])
def add_ingredient(token, category):
    """Add a new ingredient to a category (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    if category not in CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400
    
    data = request.json
    name_en = data.get("name_en", "").strip()
    name_sk = data.get("name_sk", "").strip()
    emoji = data.get("emoji", "🍕")
    
    if not name_en:
        return jsonify({"error": "English name required"}), 400
    
    # Use Slovak name same as English if not provided
    if not name_sk:
        name_sk = name_en
    
    # Generate ID from English name - sanitize to only allow alphanumeric and underscores
    ingredient_id = re.sub(r'[^a-z0-9]+', '_', name_en.lower()).strip('_')
    
    ingredients = load_ingredients()
    
    # Check if ID already exists in this category
    existing_ids = [item["id"] for item in ingredients.get(category, [])]
    if ingredient_id in existing_ids:
        return jsonify({"error": "Ingredient already exists"}), 400
    
    new_ingredient = {
        "id": ingredient_id,
        "name_en": name_en,
        "name_sk": name_sk,
        "emoji": emoji,
        "enabled": True
    }
    
    if category not in ingredients:
        ingredients[category] = []
    
    ingredients[category].append(new_ingredient)
    save_ingredients(ingredients)
    
    return jsonify({"success": True, "ingredient": new_ingredient})


@app.route("/api/ingredients/<token>/<category>/<ingredient_id>", methods=["PUT"])
def update_ingredient(token, category, ingredient_id):
    """Update an ingredient (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    if category not in CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400
    
    data = request.json
    ingredients = load_ingredients()
    
    if category not in ingredients:
        return jsonify({"error": "Category not found"}), 404
    
    # Find the ingredient
    for item in ingredients[category]:
        if item["id"] == ingredient_id:
            if "name_en" in data:
                item["name_en"] = data["name_en"]
            if "name_sk" in data:
                item["name_sk"] = data["name_sk"]
            # Support legacy "name" field for backwards compatibility
            if "name" in data and "name_en" not in data:
                item["name_en"] = data["name"]
                if "name_sk" not in item:
                    item["name_sk"] = data["name"]
            if "emoji" in data:
                item["emoji"] = data["emoji"]
            if "enabled" in data:
                item["enabled"] = data["enabled"]
            
            save_ingredients(ingredients)
            return jsonify({"success": True, "ingredient": item})
    
    return jsonify({"error": "Ingredient not found"}), 404


@app.route("/api/ingredients/<token>/<category>/<ingredient_id>", methods=["DELETE"])
def delete_ingredient(token, category, ingredient_id):
    """Delete an ingredient (admin only)."""
    if token != TOKENS["admin"]:
        return jsonify({"error": "Invalid token"}), 403
    
    if category not in CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400
    
    ingredients = load_ingredients()
    
    if category not in ingredients:
        return jsonify({"error": "Category not found"}), 404
    
    original_length = len(ingredients[category])
    ingredients[category] = [item for item in ingredients[category] if item["id"] != ingredient_id]
    
    if len(ingredients[category]) == original_length:
        return jsonify({"error": "Ingredient not found"}), 404
    
    save_ingredients(ingredients)
    return jsonify({"success": True})


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🍕 PIZZA PARTY APP RUNNING!")
    print("="*50)
    print(f"📋 Party Link: http://localhost:5000/party/{TOKENS['party']}")
    print(f"👑 Admin Link: http://localhost:5000/admin/{TOKENS['admin']}")
    print("="*50 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
