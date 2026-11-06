from django.conf import settings
from django.db import models
from apps.menu.models import Product


class Ingredient(models.Model):
    class Unit(models.TextChoices):
        KILOGRAM = 'kg', 'Kilogram (kg)'
        GRAM = 'g', 'Gram (g)'
        LITER = 'L', 'Liter (L)'
        MILLILITER = 'ml', 'Milliliter (ml)'
        PIECE = 'pcs', 'Pieces (pcs)'

    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.KILOGRAM)
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0.000,
        help_text="Current available inventory volume"
    )
    minimum_threshold = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=5.000,
        help_text="Safety stock limit triggering low-stock alert"
    )
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Procurement cost per unit in INR (₹)"
    )
    last_restocked = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_threshold

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"


class Recipe(models.Model):
    """
    Bill of Materials (BOM):
    Connects 1 menu dish to its exact ingredient recipe requirements.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_usage'
    )
    quantity_required = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        help_text="Quantity consumed per single plate/unit of this dish"
    )

    class Meta:
        unique_together = ('product', 'ingredient')

    def __str__(self):
        return f"{self.product.name} requires {self.quantity_required} {self.ingredient.unit} of {self.ingredient.name}"


class StockTransaction(models.Model):
    class TransactionType(models.TextChoices):
        INWARD_PURCHASE = 'INWARD_PURCHASE', 'Inward Stock Purchase'
        ORDER_DEDUCTION = 'ORDER_DEDUCTION', 'Order Recipe Deduction'
        SPOILAGE_LOSS = 'SPOILAGE_LOSS', 'Food Spoilage / Wastage'
        MANUAL_ADJUSTMENT = 'MANUAL_ADJUSTMENT', 'Manual Adjustment'

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        help_text="Quantity delta (positive for addition, negative for deduction)"
    )
    transaction_type = models.CharField(
        max_length=25,
        choices=TransactionType.choices,
        default=TransactionType.ORDER_DEDUCTION
    )
    reference_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='stock_deductions'
    )
    remarks = models.TextField(blank=True, null=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.quantity} {self.ingredient.unit} of {self.ingredient.name}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text="Null for all canteen administrators"
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{'Read' if self.is_read else 'Unread'}] {self.title}"
