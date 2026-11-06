import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from django.shortcuts import render, redirect, get_object_or_404
from apps.accounts.decorators import kitchen_required, admin_required
from apps.inventory.models import Recipe, Ingredient, StockTransaction, Notification
from apps.menu.models import Product
from .models import Order, OrderItem, Payment


def get_cart(session):
    return session.get('cart', {})


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = request.session.get('cart', {})
    p_id = str(product_id)

    if p_id in cart:
        cart[p_id]['quantity'] += 1
    else:
        cart[p_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to your tray.")
    return redirect(request.META.get('HTTP_REFERER', 'menu:customer_menu'))


def remove_from_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    if p_id in cart:
        if cart[p_id]['quantity'] > 1:
            cart[p_id]['quantity'] -= 1
        else:
            del cart[p_id]
        request.session['cart'] = cart
        messages.info(request, "Tray updated.")
    return redirect('orders:cart_view')


def cart_view(request):
    cart = get_cart(request.session)
    cart_items = []
    total_price = 0.0

    for p_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        cart_items.append({
            'product_id': p_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'table_number': request.session.get('table_number', 'Takeaway')
    })


@login_required
def checkout_order_view(request):
    cart = get_cart(request.session)
    if not cart:
        messages.warning(request, "Your cart is empty. Please select food items first.")
        return redirect('menu:customer_menu')

    payment_mode = request.POST.get('payment_mode', Payment.Mode.UPI_MOCK)
    table_num = request.session.get('table_number', 'Takeaway')
    notes = request.POST.get('notes', '')

    with transaction.atomic():
        total_amount = sum(item['price'] * item['quantity'] for item in cart.values())

        # Create Order
        order = Order.objects.create(
            user=request.user,
            table_number=table_num,
            total_amount=total_amount,
            status=Order.Status.PENDING,
            notes=notes
        )

        # Create Order Items
        for p_id, item in cart.items():
            product = Product.objects.get(id=int(p_id))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                unit_price=item['price']
            )

        # Create Payment Record
        Payment.objects.create(
            order=order,
            amount=total_amount,
            payment_mode=payment_mode,
            transaction_ref=f"TXN-{uuid.uuid4().hex[:10].upper()}",
            payment_status=Payment.Status.SUCCESS
        )

        # Clear session cart
        request.session['cart'] = {}

    messages.success(request, f"Order placed successfully! Token: {order.order_token}")
    return redirect('orders:order_detail', order_token=order.order_token)


def order_detail_view(request, order_token):
    order = get_object_or_404(Order, order_token=order_token)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@kitchen_required
def kds_board_view(request):
    """
    Live Kitchen Display System (KDS) board.
    Shows active orders categorized by status.
    """
    pending_orders = Order.objects.filter(status=Order.Status.PENDING).order_by('created_at')
    preparing_orders = Order.objects.filter(status__in=[Order.Status.CONFIRMED, Order.Status.PREPARING]).order_by('created_at')
    ready_orders = Order.objects.filter(status=Order.Status.READY).order_by('-updated_at')[:10]

    return render(request, 'orders/kds_board.html', {
        'pending_orders': pending_orders,
        'preparing_orders': preparing_orders,
        'ready_orders': ready_orders,
    })


@kitchen_required
def update_order_status_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    next_status = request.POST.get('status')

    if next_status in Order.Status.values:
        with transaction.atomic():
            # If advancing to CONFIRMED, execute recipe BOM stock deduction
            if next_status == Order.Status.CONFIRMED and order.status == Order.Status.PENDING:
                for item in order.items.all():
                    recipes = Recipe.objects.filter(product=item.product)
                    for recipe in recipes:
                        ing = recipe.ingredient
                        deduction_qty = recipe.quantity_required * item.quantity
                        ing.current_stock -= deduction_qty
                        ing.save(update_fields=['current_stock'])

                        # Record transaction audit
                        StockTransaction.objects.create(
                            ingredient=ing,
                            quantity=-deduction_qty,
                            transaction_type=StockTransaction.TransactionType.ORDER_DEDUCTION,
                            reference_order=order,
                            remarks=f"Deducted for order {order.order_token}"
                        )

                        # Trigger threshold alert if breached
                        if ing.is_low_stock:
                            Notification.objects.create(
                                title=f"Low Stock Alert: {ing.name}",
                                message=f"Remaining stock for {ing.name} is down to {ing.current_stock} {ing.unit} (Threshold: {ing.minimum_threshold} {ing.unit})."
                            )

            order.status = next_status
            order.save(update_fields=['status', 'updated_at'])
            messages.success(request, f"Order {order.order_token} updated to {order.get_status_display()}")

    return redirect('orders:kds_board')


@admin_required
def admin_dashboard_view(request):
    recent_orders = Order.objects.all().order_by('-created_at')[:8]
    total_revenue = sum(o.total_amount for o in Order.objects.filter(status=Order.Status.COMPLETED))
    today_orders_count = Order.objects.count()
    low_stock_count = Ingredient.objects.filter(current_stock__lte=models.F('minimum_threshold')).count()

    return render(request, 'orders/admin_dashboard.html', {
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'today_orders_count': today_orders_count,
        'low_stock_count': low_stock_count,
    })
