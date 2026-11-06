import uuid
from django.conf import settings
from django.db import models
from apps.menu.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending (Submitted)'
        CONFIRMED = 'CONFIRMED', 'Confirmed (Accepted by Kitchen)'
        PREPARING = 'PREPARING', 'Preparing in Kitchen'
        READY = 'READY', 'Ready for Collection'
        COMPLETED = 'COMPLETED', 'Completed / Collected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    order_token = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Public cafeteria order token, e.g. SC-104"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    table_number = models.CharField(
        max_length=20,
        default="Takeaway",
        help_text="Table number scanned via QR or Takeaway counter"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    notes = models.TextField(blank=True, null=True, help_text="Special dietary or preparation instructions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_token:
            # Generate short, human-readable token like SC-1234
            unique_part = str(uuid.uuid4().int)[:4]
            self.order_token = f"SC-{unique_part}"
        super().save(*args, **kwargs)

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total

    def __str__(self):
        return f"{self.order_token} - {self.user.username} ({self.get_status_display()})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} ({self.order.order_token})"


class Payment(models.Model):
    class Mode(models.TextChoices):
        UPI_MOCK = 'UPI_MOCK', 'Simulated UPI (GPay/Paytm/PhonePe)'
        STUDENT_WALLET = 'STUDENT_WALLET', 'Campus Student Wallet'
        CASH = 'CASH', 'Cash at Counter'

    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Payment Successful'
        PENDING = 'PENDING', 'Payment Pending'
        FAILED = 'FAILED', 'Payment Failed'

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(
        max_length=20,
        choices=Mode.choices,
        default=Mode.UPI_MOCK
    )
    transaction_ref = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUCCESS
    )
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_ref} for {self.order.order_token} - {self.get_payment_status_display()}"
