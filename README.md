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

PythonAnywhere offers free hosting for Python web apps - perfect for your pizza party!

### 1. Create a PythonAnywhere Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free "Beginner" account
3. Your app will be available at `yourusername.pythonanywhere.com`

### 2. Upload Your Files

**Option A: Upload via Files Tab**

1. Go to the **Files** tab
2. Navigate to `/home/yourusername/`
3. Create a new directory called `pizza-party`
4. Upload all project files (`app.py`, `requirements.txt`, `translations.json`, and the `templates/` folder)

**Option B: Clone from Git (if hosted on GitHub)**

1. Open a **Bash console** from the Consoles tab
2. Run:
   ```bash
   cd ~
   git clone https://github.com/yourusername/pizza-party.git
   ```

### 3. Set Up Virtual Environment

In a Bash console:

```bash
cd ~/pizza-party
mkvirtualenv --python=/usr/bin/python3.10 pizza-env
pip install -r requirements.txt
```

### 4. Create the Web App

1. Go to the **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Flask - we'll configure it ourselves)
4. Select **Python 3.10**

### 5. Configure the Web App

On the Web tab, set these values:

**Source code:** `/home/yourusername/pizza-party`

**Working directory:** `/home/yourusername/pizza-party`

**Virtualenv:** `/home/yourusername/.virtualenvs/pizza-env`

### 6. Edit the WSGI File

Click on the **WSGI configuration file** link (something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)

Replace ALL the contents with:

```python
import sys
import os

# Add your project directory to the path
project_home = '/home/yourusername/pizza-party'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Change to the project directory (so JSON files are created in the right place)
os.chdir(project_home)

# Import your Flask app
from app import app as application
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

### 7. Reload and Launch

1. Go back to the **Web** tab
2. Click the green **Reload** button
3. Visit `https://yourusername.pythonanywhere.com`

### 8. Get Your Links

Since PythonAnywhere doesn't show console output, you need to find your tokens:

1. Go to the **Files** tab
2. Navigate to `/home/yourusername/pizza-party/`
3. Click on `tokens.json` to view it
4. Your links will be:
   - **Party Link:** `https://yourusername.pythonanywhere.com/party/YOUR_PARTY_TOKEN`
   - **Admin Link:** `https://yourusername.pythonanywhere.com/admin/YOUR_ADMIN_TOKEN`

### Troubleshooting

**App not loading?**
- Check the **Error log** link on the Web tab
- Make sure the WSGI file has the correct paths
- Ensure the virtualenv path is correct

**Files not found?**
- Make sure `os.chdir(project_home)` is in your WSGI file
- Check that all files were uploaded to the correct directory

**Changes not showing?**
- Always click **Reload** on the Web tab after making changes

### Updating the App

1. Upload new files or `git pull` in a Bash console
2. Click **Reload** on the Web tab
3. That's it!

## Tips for Your Party

1. 🖨️ Print a QR code for the party link
2. 📺 Display the admin page on a TV
3. ⏰ Set a deadline for orders
4. 🍕 Have fun making pizzas!

---

Made with 🍕 and ❤️ for pizza lovers everywhere!
