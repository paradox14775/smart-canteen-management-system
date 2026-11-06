from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student / Customer'
        ADMIN = 'ADMIN', 'Canteen Administrator'
        KITCHEN = 'KITCHEN', 'Kitchen Staff'
        MANAGEMENT = 'MANAGEMENT', 'Management / Analyst'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Designated role in Smart Canteen Management System"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_canteen_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_kitchen_staff(self):
        return self.role == self.Role.KITCHEN

    @property
    def is_management_analyst(self):
        return self.role == self.Role.MANAGEMENT or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    enrollment_no = models.CharField(
        max_length=30,
        unique=True,
        help_text="University Enrollment / Roll Number"
    )
    course = models.CharField(
        max_length=100,
        default="MCA",
        help_text="Program / Department (e.g., MCA, B.Tech, BCA)"
    )
    semester = models.IntegerField(default=1)
    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500.00,
        help_text="Mock digital wallet balance for cafeteria purchases"
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.enrollment_no})"
