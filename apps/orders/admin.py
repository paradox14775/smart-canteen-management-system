from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_token', 'user', 'table_number', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'table_number', 'created_at')
    search_fields = ('order_token', 'user__username', 'table_number')
    inlines = (OrderItemInline, PaymentInline)
    list_editable = ('status',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_ref', 'order', 'amount', 'payment_mode', 'payment_status', 'paid_at')
    list_filter = ('payment_mode', 'payment_status', 'paid_at')
    search_fields = ('transaction_ref', 'order__order_token')
