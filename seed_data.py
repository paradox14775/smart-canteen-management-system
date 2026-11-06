"""
Seed script to populate initial users, menu categories, dishes, ingredients,
recipes (BOM), table QR codes, and ML demand forecasts for the Smart Canteen Management System.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_canteen.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import StudentProfile
from apps.menu.models import Category, Product, TableQR
from apps.inventory.models import Ingredient, Recipe, StockTransaction
from apps.analytics.ml_service import train_and_forecast_demand

User = get_user_model()


def seed_database():
    print("[*] Starting Smart Canteen Database Seeder...")

    # 1. Seed Roles & Users
    users_to_create = [
        {"username": "admin", "email": "admin@canteen.ipu.ac.in", "role": User.Role.ADMIN, "first": "Campus", "last": "Admin", "pass": "admin123", "is_super": True},
        {"username": "chef", "email": "kitchen@canteen.ipu.ac.in", "role": User.Role.KITCHEN, "first": "Executive", "last": "Chef", "pass": "chef123", "is_super": False},
        {"username": "student", "email": "student@ipu.ac.in", "role": User.Role.STUDENT, "first": "Rahul", "last": "Sharma", "pass": "student123", "is_super": False},
        {"username": "manager", "email": "management@ipu.ac.in", "role": User.Role.MANAGEMENT, "first": "Priya", "last": "Verma", "pass": "manager123", "is_super": False},
    ]

    for u in users_to_create:
        user_obj, created = User.objects.get_or_create(
            username=u["username"],
            defaults={
                "email": u["email"],
                "role": u["role"],
                "first_name": u["first"],
                "last_name": u["last"],
                "is_staff": u["is_super"] or u["role"] == User.Role.ADMIN,
                "is_superuser": u["is_super"],
            }
        )
        if created:
            user_obj.set_password(u["pass"])
            user_obj.save()
            print(f"  + User created: {u['username']} ({u['role']})")
            if u["role"] == User.Role.STUDENT:
                StudentProfile.objects.get_or_create(
                    user=user_obj,
                    defaults={
                        "enrollment_no": "01216404423",
                        "course": "MCA",
                        "semester": 3,
                        "wallet_balance": 500.00
                    }
                )

    # 2. Seed Categories
    cat_meals, _ = Category.objects.get_or_create(name="Meals & Combos", defaults={"description": "Wholesome lunch meals and traditional platters", "icon": "bi-egg-fried"})
    cat_snacks, _ = Category.objects.get_or_create(name="Snacks & Quick Bites", defaults={"description": "Fresh hot fried items, sandwiches and puffs", "icon": "bi-pie-chart"})
    cat_drinks, _ = Category.objects.get_or_create(name="Beverages", defaults={"description": "Hot brewed teas, milkshakes, and chilled coolers", "icon": "bi-cup-straw"})
    cat_desserts, _ = Category.objects.get_or_create(name="Desserts", defaults={"description": "Sweet indulgences and bakery treats", "icon": "bi-cake2"})
    print("  + Categories seeded.")

    # 3. Seed Products
    products_data = [
        {"name": "Paneer Thali Deluxe", "category": cat_meals, "price": 120.00, "prep": 12, "desc": "Shahi paneer, 3 butter rotis, dal tadka, jeera rice, and salad."},
        {"name": "Dal Makhani Rice Combo", "category": cat_meals, "price": 90.00, "prep": 10, "desc": "Creamy slow-cooked dal makhani served over aromatic basmati rice."},
        {"name": "Crispy Aloo Samosa (2 Pcs)", "category": cat_snacks, "price": 25.00, "prep": 5, "desc": "Crispy golden pastry stuffed with spiced potato mash and green peas."},
        {"name": "Veg Grilled Club Sandwich", "category": cat_snacks, "price": 55.00, "prep": 8, "desc": "Triple layered sandwich with cucumber, tomato, potato mash, and mint chutney."},
        {"name": "Masala Chai", "category": cat_drinks, "price": 15.00, "prep": 4, "desc": "Traditional ginger and cardamom infused milk tea."},
        {"name": "Cold Coffee Frappe", "category": cat_drinks, "price": 45.00, "prep": 5, "desc": "Chilled blended espresso with fresh milk and chocolate syrup."},
        {"name": "Chocolate Walnut Brownie", "category": cat_desserts, "price": 60.00, "prep": 2, "desc": "Warm fudge brownie with toasted walnuts."},
    ]

    product_objs = {}
    for p in products_data:
        prod, _ = Product.objects.get_or_create(
            name=p["name"],
            defaults={
                "category": p["category"],
                "price": p["price"],
                "preparation_time": p["prep"],
                "description": p["desc"],
                "is_available": True
            }
        )
        product_objs[p["name"]] = prod
    print("  + Menu products seeded.")

    # 4. Seed Raw Ingredients
    ingredients_data = [
        {"name": "Potatoes", "unit": Ingredient.Unit.KILOGRAM, "stock": 45.0, "threshold": 10.0, "cost": 25.0},
        {"name": "Flour (Maida)", "unit": Ingredient.Unit.KILOGRAM, "stock": 35.0, "threshold": 8.0, "cost": 36.0},
        {"name": "Cooking Oil", "unit": Ingredient.Unit.LITER, "stock": 30.0, "threshold": 6.0, "cost": 125.0},
        {"name": "Full Cream Milk", "unit": Ingredient.Unit.LITER, "stock": 25.0, "threshold": 8.0, "cost": 62.0},
        {"name": "Fresh Paneer", "unit": Ingredient.Unit.KILOGRAM, "stock": 18.0, "threshold": 4.0, "cost": 340.0},
        {"name": "Assam Tea Leaves", "unit": Ingredient.Unit.KILOGRAM, "stock": 6.0, "threshold": 1.5, "cost": 290.0},
        {"name": "Coffee Beans / Powder", "unit": Ingredient.Unit.KILOGRAM, "stock": 5.0, "threshold": 1.0, "cost": 650.0},
        {"name": "Sandwich Bread", "unit": Ingredient.Unit.PIECE, "stock": 30.0, "threshold": 8.0, "cost": 3.0},
    ]

    ing_objs = {}
    for ing in ingredients_data:
        i_obj, _ = Ingredient.objects.get_or_create(
            name=ing["name"],
            defaults={
                "unit": ing["unit"],
                "current_stock": ing["stock"],
                "minimum_threshold": ing["threshold"],
                "unit_cost": ing["cost"]
            }
        )
        ing_objs[ing["name"]] = i_obj
    print("  + Raw material inventory seeded.")

    # 5. Seed Recipe BOM Mappings
    recipes_data = [
        # Samosa: 0.15kg potatoes, 0.05kg flour, 0.02L oil
        (product_objs["Crispy Aloo Samosa (2 Pcs)"], ing_objs["Potatoes"], 0.150),
        (product_objs["Crispy Aloo Samosa (2 Pcs)"], ing_objs["Flour (Maida)"], 0.050),
        (product_objs["Crispy Aloo Samosa (2 Pcs)"], ing_objs["Cooking Oil"], 0.020),
        # Masala Chai: 0.15L milk, 0.01kg tea leaves
        (product_objs["Masala Chai"], ing_objs["Full Cream Milk"], 0.150),
        (product_objs["Masala Chai"], ing_objs["Assam Tea Leaves"], 0.010),
        # Cold Coffee: 0.20L milk, 0.015kg coffee
        (product_objs["Cold Coffee Frappe"], ing_objs["Full Cream Milk"], 0.200),
        (product_objs["Cold Coffee Frappe"], ing_objs["Coffee Beans / Powder"], 0.015),
        # Paneer Thali: 0.15kg paneer, 0.03L oil
        (product_objs["Paneer Thali Deluxe"], ing_objs["Fresh Paneer"], 0.150),
        (product_objs["Paneer Thali Deluxe"], ing_objs["Cooking Oil"], 0.030),
        # Sandwich: 2 bread slices, 0.06kg potatoes
        (product_objs["Veg Grilled Club Sandwich"], ing_objs["Sandwich Bread"], 2.0),
        (product_objs["Veg Grilled Club Sandwich"], ing_objs["Potatoes"], 0.060),
    ]

    for prod, ing, qty in recipes_data:
        Recipe.objects.get_or_create(
            product=prod,
            ingredient=ing,
            defaults={"quantity_required": qty}
        )
    print("  + Recipe BOM mappings seeded.")

    # 6. Seed Table QR Placards
    tables = ["Table-01", "Table-02", "Table-03", "Counter-A"]
    for t in tables:
        t_obj, _ = TableQR.objects.get_or_create(table_number=t)
    print("  + Table QR placards initialized.")

    # 7. Execute Initial ML Demand Forecasting Model
    print("  + Running Scikit-learn demand forecasting training...")
    ml_res = train_and_forecast_demand()
    print(f"  + ML Status: {ml_res.get('status')} for target date {ml_res.get('forecast_date')}")

    print("\n[+] Database seeding complete! All modules, roles, and models are operational.")


if __name__ == '__main__':
    seed_database()
