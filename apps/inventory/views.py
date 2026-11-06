from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.accounts.decorators import admin_required
from .models import Ingredient, Recipe, StockTransaction, Notification
from apps.menu.models import Product


@admin_required
def inventory_list_view(request):
    ingredients = Ingredient.objects.all().order_by('name')
    notifications = Notification.objects.filter(is_read=False)[:5]

    if request.method == 'POST':
        # Quick Inward Stock Restock
        ingredient_id = request.POST.get('ingredient_id')
        qty = Decimal(request.POST.get('quantity', '0'))
        if ingredient_id and qty > 0:
            ing = get_object_or_404(Ingredient, id=ingredient_id)
            ing.current_stock += qty
            ing.save(update_fields=['current_stock', 'last_restocked'])

            StockTransaction.objects.create(
                ingredient=ing,
                quantity=qty,
                transaction_type=StockTransaction.TransactionType.INWARD_PURCHASE,
                remarks="Manual inward stock entry via admin portal"
            )
            messages.success(request, f"Successfully restocked {qty} {ing.unit} of {ing.name}.")
            return redirect('inventory:list')

    return render(request, 'inventory/inventory_list.html', {
        'ingredients': ingredients,
        'notifications': notifications
    })


@admin_required
def recipe_list_view(request):
    products = Product.objects.all().prefetch_related('recipes__ingredient')
    ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        ingredient_id = request.POST.get('ingredient_id')
        qty = Decimal(request.POST.get('quantity_required', '0.1'))

        if product_id and ingredient_id and qty > 0:
            product = get_object_or_404(Product, id=product_id)
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            Recipe.objects.update_or_create(
                product=product,
                ingredient=ingredient,
                defaults={'quantity_required': qty}
            )
            messages.success(request, f"Recipe BOM updated for {product.name} -> {ingredient.name} ({qty} {ingredient.unit})")
            return redirect('inventory:recipes')

    return render(request, 'inventory/recipe_list.html', {
        'products': products,
        'ingredients': ingredients
    })


@admin_required
def stock_transactions_log_view(request):
    transactions = StockTransaction.objects.all().select_related('ingredient', 'reference_order')[:50]
    return render(request, 'inventory/stock_transactions.html', {
        'transactions': transactions
    })
