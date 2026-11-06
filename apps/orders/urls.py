from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_order_view, name='checkout'),
    path('status/<str:order_token>/', views.order_detail_view, name='order_detail'),
    path('history/', views.order_history_view, name='order_history'),
    path('kds/', views.kds_board_view, name='kds_board'),
    path('kds/update/<int:order_id>/', views.update_order_status_view, name='update_order_status'),
    path('admin-portal/', views.admin_dashboard_view, name='admin_dashboard'),
]
