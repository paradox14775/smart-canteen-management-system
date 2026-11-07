from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list_view, name='list'),
    path('recipes/', views.recipe_list_view, name='recipes'),
    path('logs/', views.stock_transactions_log_view, name='logs'),
]

