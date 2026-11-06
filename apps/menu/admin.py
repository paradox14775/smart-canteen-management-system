from django.contrib import admin
from .models import Category, Product, TableQR


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'preparation_time', 'is_available', 'updated_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')


@admin.register(TableQR)
class TableQRAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'is_active', 'created_at')
    list_filter = ('is_active',)
