from django.db import models
from apps.menu.models import Product


class DemandForecast(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='forecasts'
    )
    forecast_date = models.DateField(help_text="Target date for forecasted demand")
    predicted_quantity = models.PositiveIntegerField(help_text="Estimated units to prepare")
    actual_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Realized units sold (updated post-business day)"
    )
    model_name = models.CharField(
        max_length=60,
        default="RandomForestRegressor",
        help_text="Machine learning model architecture"
    )
    mae_score = models.FloatField(null=True, blank=True, help_text="Mean Absolute Error of the trained model")
    rmse_score = models.FloatField(null=True, blank=True, help_text="Root Mean Squared Error")
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-forecast_date', 'product']
        unique_together = ('product', 'forecast_date', 'model_name')

    def __str__(self):
        return f"{self.product.name} on {self.forecast_date}: {self.predicted_quantity} units ({self.model_name})"
