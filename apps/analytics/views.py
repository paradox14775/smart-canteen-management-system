import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.shortcuts import render, redirect
from apps.accounts.decorators import management_required
from apps.analytics.models import DemandForecast
from apps.analytics.ml_service import train_and_forecast_demand
from apps.menu.models import Product, Category
from apps.orders.models import Order, OrderItem


@management_required
def analytics_dashboard_view(request):
    """
    Management & Business Intelligence Dashboard.
    Provides financial KPIs, category distribution, sales trends, and ML demand forecasts.
    """
    total_revenue = Order.objects.filter(status=Order.Status.COMPLETED).aggregate(
        total=Sum('total_amount')
    )['total'] or 0.00

    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status=Order.Status.COMPLETED).count()
    avg_order_value = Order.objects.filter(status=Order.Status.COMPLETED).aggregate(
        avg=Avg('total_amount')
    )['avg'] or 0.00

    # Top 5 Best Selling Items
    top_products = OrderItem.objects.values(
        'product__name'
    ).annotate(
        total_qty=Sum('quantity'),
        total_sales=Sum('unit_price')
    ).order_by('-total_qty')[:5]

    # Category Revenue Distribution
    category_sales = OrderItem.objects.values(
        'product__category__name'
    ).annotate(
        total_sales=Sum('unit_price')
    ).order_by('-total_sales')

    cat_labels = [c['product__category__name'] or 'General' for c in category_sales]
    cat_data = [float(c['total_sales'] or 0) for c in category_sales]

    # Fallback chart data if fresh database
    if not cat_labels:
        cat_labels = ['Meals', 'Snacks', 'Beverages', 'Desserts']
        cat_data = [4500.0, 3200.0, 2100.0, 1100.0]

    # Hourly Peak Order Congestion Simulation / Data
    hours_labels = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM']
    hourly_orders = [12, 28, 65, 142, 185, 94, 38, 22]

    # Latest ML Forecasts
    forecasts = DemandForecast.objects.all().select_related('product')[:10]

    return render(request, 'analytics/dashboard.html', {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'avg_order_value': round(avg_order_value, 2),
        'top_products': top_products,
        'forecasts': forecasts,
        'cat_labels_json': json.dumps(cat_labels),
        'cat_data_json': json.dumps(cat_data),
        'hours_labels_json': json.dumps(hours_labels),
        'hourly_orders_json': json.dumps(hourly_orders),
    })


@management_required
def trigger_ml_training_view(request):
    result = train_and_forecast_demand()
    if result.get('status') == 'success':
        messages.success(
            request,
            f"Machine Learning pipeline executed successfully! Forecasts generated for {result.get('forecast_date')}."
        )
    else:
        messages.error(request, result.get('message', 'Training failed.'))

    return redirect('analytics:dashboard')
