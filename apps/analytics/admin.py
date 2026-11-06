from django.contrib import admin
from .models import DemandForecast


@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = ('product', 'forecast_date', 'predicted_quantity', 'actual_quantity', 'model_name', 'mae_score', 'generated_at')
    list_filter = ('forecast_date', 'model_name')
    search_fields = ('product__name',)
