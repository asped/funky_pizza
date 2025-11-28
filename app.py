"""
🍕 Pizza Party Order App
A simple Flask app for ordering pizzas at a party!
"""

import json
import os
import secrets
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# File to store orders
ORDERS_FILE = "orders.json"

# Generate tokens on first run or load existing ones
TOKENS_FILE = "tokens.json"

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

TOKENS = load_tokens()

# Available ingredients
INGREDIENTS = {
    "sauces": [
        {"id": "tomato", "name": "Tomato Sauce", "emoji": "🍅"},
        {"id": "white", "name": "White/Cream Sauce", "emoji": "🥛"},
        {"id": "bbq", "name": "BBQ Sauce", "emoji": "🔥"},
        {"id": "pesto", "name": "Pesto", "emoji": "🌿"},
    ],
    "cheeses": [
        {"id": "mozzarella", "name": "Mozzarella", "emoji": "🧀"},
        {"id": "parmesan", "name": "Parmesan", "emoji": "🧀"},
        {"id": "gorgonzola", "name": "Gorgonzola", "emoji": "🧀"},
        {"id": "goat", "name": "Goat Cheese", "emoji": "🐐"},
    ],
    "meats": [
        {"id": "pepperoni", "name": "Pepperoni", "emoji": "🍖"},
        {"id": "ham", "name": "Ham", "emoji": "🐷"},
        {"id": "bacon", "name": "Bacon", "emoji": "🥓"},
        {"id": "sausage", "name": "Italian Sausage", "emoji": "🌭"},
        {"id": "chicken", "name": "Chicken", "emoji": "🍗"},
    ],
    "veggies": [
        {"id": "mushrooms", "name": "Mushrooms", "emoji": "🍄"},
        {"id": "onions", "name": "Onions", "emoji": "🧅"},
        {"id": "peppers", "name": "Bell Peppers", "emoji": "🫑"},
        {"id": "olives", "name": "Olives", "emoji": "🫒"},
        {"id": "tomatoes", "name": "Fresh Tomatoes", "emoji": "🍅"},
        {"id": "spinach", "name": "Spinach", "emoji": "🥬"},
        {"id": "jalapenos", "name": "Jalapeños", "emoji": "🌶️"},
        {"id": "pineapple", "name": "Pineapple", "emoji": "🍍"},
        {"id": "arugula", "name": "Arugula", "emoji": "🥗"},
    ],
    "extras": [
        {"id": "garlic", "name": "Extra Garlic", "emoji": "🧄"},
        {"id": "basil", "name": "Fresh Basil", "emoji": "🌿"},
        {"id": "oregano", "name": "Oregano", "emoji": "🌱"},
        {"id": "chili", "name": "Chili Flakes", "emoji": "🌶️"},
        {"id": "truffle", "name": "Truffle Oil", "emoji": "✨"},
    ]
}


def load_orders():
    """Load orders from JSON file."""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_orders(orders):
    """Save orders to JSON file."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)


@app.route("/")
def home():
    """Redirect to nowhere - need token to access."""
    return "🍕 Pizza Party! You need a valid link to join.", 403


@app.route("/party/<token>")
def party(token):
    """Main party page - order your pizza!"""
    if token != TOKENS["party"]:
        return "🚫 Invalid party link!", 403
    return render_template("index.html", token=token, ingredients=INGREDIENTS)


@app.route("/admin/<token>")
def admin(token):
    """Admin page - see all orders."""
    if token != TOKENS["admin"]:
        return "🚫 Invalid admin link!", 403
    orders = load_orders()
    return render_template("admin.html", orders=orders, ingredients=INGREDIENTS)


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
    
    if not name:
        return jsonify({"error": "Name required"}), 400
    
    orders = load_orders()
    orders[name] = {
        "display_name": data.get("name", "").strip(),  # Keep original case for display
        "ingredients": ingredients
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


if __name__ == "__main__":
    # Print tokens on startup
    print("\n" + "="*50)
    print("🍕 PIZZA PARTY APP RUNNING!")
    print("="*50)
    print(f"📋 Party Link: http://localhost:5000/party/{TOKENS['party']}")
    print(f"👑 Admin Link: http://localhost:5000/admin/{TOKENS['admin']}")
    print("="*50 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
