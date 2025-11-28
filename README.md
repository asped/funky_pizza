# 🍕 Pizza Party Order App

A fun, simple web app for ordering pizzas at your party! Each guest can build their own dream pizza, and the admin can see all orders at a glance.

![Pizza Party](https://img.shields.io/badge/Party-Mode-orange?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNiAzNiI+PHBhdGggZmlsbD0iI0ZGQ0MwMCIgZD0iTTM1IDE4YzAgOS4zODktNy42MTEgMTctMTcgMTdTMSAyNy4zODkgMSAxOCAxOS42MTEgMSAxOCAxczE3IDcuNjExIDE3IDE3eiIvPjwvc3ZnPg==)

## Features

- 🎉 **Simple party mode** - Share a link, guests enter their name, done!
- 🍕 **Build your pizza** - Choose from sauces, cheeses, meats, veggies & extras
- 👑 **Admin dashboard** - See all orders in a beautiful dark-mode interface
- 🔒 **Token-based access** - No login required, just share the magic links
- 💾 **Auto-save orders** - Orders persist in a simple JSON file
- 📱 **Mobile-friendly** - Works great on phones and tablets

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
python app.py
```

### 3. Get your links

When the app starts, it will print two links:

```
==================================================
🍕 PIZZA PARTY APP RUNNING!
==================================================
📋 Party Link: http://localhost:5000/party/abc123...
👑 Admin Link: http://localhost:5000/admin/xyz789...
==================================================
```

- **Party Link** - Share this with your guests
- **Admin Link** - Keep this for yourself to see all orders

## How It Works

### For Guests

1. Open the party link
2. Enter your name
3. Select your pizza ingredients
4. Click "Save My Pizza!"
5. Done! Come back anytime to modify your order

### For Admin

1. Open the admin link
2. See all orders in real-time
3. Orders auto-refresh every 30 seconds
4. Delete orders if needed

## Available Ingredients

### 🍅 Sauces
Tomato, White/Cream, BBQ, Pesto

### 🧀 Cheeses
Mozzarella, Parmesan, Gorgonzola, Goat Cheese

### 🥓 Meats
Pepperoni, Ham, Bacon, Italian Sausage, Chicken

### 🥬 Veggies
Mushrooms, Onions, Bell Peppers, Olives, Fresh Tomatoes, Spinach, Jalapeños, Pineapple, Arugula

### ✨ Extras
Extra Garlic, Fresh Basil, Oregano, Chili Flakes, Truffle Oil

## Customization

### Adding/Removing Ingredients

Edit the `INGREDIENTS` dictionary in `app.py`:

```python
INGREDIENTS = {
    "sauces": [
        {"id": "tomato", "name": "Tomato Sauce", "emoji": "🍅"},
        # Add more sauces here...
    ],
    # ...
}
```

### Changing Tokens

Delete `tokens.json` and restart the app to generate new tokens.

Or manually edit `tokens.json`:

```json
{
  "party": "your-custom-party-token",
  "admin": "your-custom-admin-token"
}
```

## File Structure

```
pizza-party/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── orders.json         # Stored orders (auto-created)
├── tokens.json         # Access tokens (auto-created)
├── templates/
│   ├── index.html      # Guest ordering page
│   └── admin.html      # Admin dashboard
└── README.md
```

## Tech Stack

- **Backend**: Python + Flask
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Storage**: JSON file (no database needed)
- **Fonts**: Fredoka + Nunito (Google Fonts)

## Deploying to PythonAnywhere

This project includes a GitHub Actions workflow for automatic deployment.

### 1. Get Your PythonAnywhere API Token

1. Create an account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to **Account** → **API token**
3. Click **Create a new API token** and copy it

### 2. Set Up GitHub Secrets

In your GitHub repository, go to **Settings** → **Secrets and variables** → **Actions**, and add:

| Secret Name | Value |
|-------------|-------|
| `PYTHONANYWHERE_API_USER` | Your PythonAnywhere username |
| `PYTHONANYWHERE_API_TOKEN` | Your API token from step 1 |

Now every push to `master` will automatically deploy to PythonAnywhere! 🚀

## Tips for Your Party

1. 🖨️ Print a QR code for the party link
2. 📺 Display the admin page on a TV
3. ⏰ Set a deadline for orders
4. 🍕 Have fun making pizzas!

---

Made with 🍕 and ❤️ for pizza lovers everywhere!
