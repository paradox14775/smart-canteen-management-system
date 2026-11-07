from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard_view, name='dashboard'),
    path('train-ml/', views.trigger_ml_training_view, name='train_ml'),
]

