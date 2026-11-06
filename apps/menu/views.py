from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.accounts.decorators import admin_required
from .models import Category, Product, TableQR


def customer_menu_view(request):
    """
    Mobile-first customer menu accessed via QR scan or web portal.
    Handles table attribution from ?table=T-01
    """
    table_num = request.GET.get('table', request.session.get('table_number', 'Takeaway'))
    request.session['table_number'] = table_num

    categories = Category.objects.filter(is_active=True).prefetch_related('products')
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()

    products = Product.objects.filter(is_available=True)
    if selected_category:
        products = products.filter(category__id=selected_category)
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'menu/customer_menu.html', {
        'categories': categories,
        'products': products,
        'table_number': table_num,
        'search_query': search_query,
        'selected_category': selected_category,
    })


@admin_required
def admin_menu_manage_view(request):
    categories = Category.objects.all()
    products = Product.objects.all().select_related('category')
    return render(request, 'menu/admin_manage.html', {
        'categories': categories,
        'products': products
    })


@admin_required
def table_qr_list_view(request):
    tables = TableQR.objects.all().order_by('table_number')
    if request.method == 'POST':
        table_name = request.POST.get('table_number', '').strip()
        if table_name:
            TableQR.objects.get_or_create(table_number=table_name)
            messages.success(request, f"QR code generated for {table_name}")
            return redirect('menu:table_qr_list')

    return render(request, 'menu/table_qr_list.html', {
        'tables': tables
    })
