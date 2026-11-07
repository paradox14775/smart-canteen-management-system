from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.customer_menu_view, name='customer_menu'),
    path('manage/', views.admin_menu_manage_view, name='admin_menu_manage'),
    path('qr-codes/', views.table_qr_list_view, name='table_qr_list'),
]

