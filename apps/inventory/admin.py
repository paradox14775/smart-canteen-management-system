from django.contrib import admin
from .models import Ingredient, Recipe, StockTransaction, Notification


class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_stock', 'unit', 'minimum_threshold', 'unit_cost', 'is_low_stock', 'last_restocked')
    list_filter = ('unit',)
    search_fields = ('name',)
    list_editable = ('current_stock', 'minimum_threshold', 'unit_cost')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredient', 'quantity_required')
    list_filter = ('product__category', 'ingredient')
    search_fields = ('product__name', 'ingredient__name')


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity', 'transaction_type', 'reference_order', 'logged_at')
    list_filter = ('transaction_type', 'logged_at')
    search_fields = ('ingredient__name', 'reference_order__order_token')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message')
