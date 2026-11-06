import io
import qrcode
from django.core.files.base import ContentFile
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default="bi-cup-hot", help_text="Bootstrap icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.PositiveIntegerField(
        default=10,
        help_text="Estimated preparation time in minutes"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Live stock availability toggle for kitchen"
    )
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class TableQR(models.Model):
    table_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Table or Counter designation, e.g. T-01, Counter-A"
    )
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_qr_code(self, base_url="http://127.0.0.1:8000"):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        target_url = f"{base_url}/order/?table={self.table_number}"
        qr.add_data(target_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        filename = f"qr_{self.table_number}.png"
        self.qr_image.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_image:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number}"
