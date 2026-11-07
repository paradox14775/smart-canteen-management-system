import datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from apps.analytics.models import DemandForecast
from apps.menu.models import Product
from apps.orders.models import Order, OrderItem


def train_and_forecast_demand():
    """
    Scikit-learn demand forecasting pipeline.
    Uses historical cafeteria orders or realistic collegiate distribution
    to train regression models and generate next-day dish demand estimates.
    """
    products = Product.objects.all()
    if not products.exists():
        return {"status": "error", "message": "No menu products available for training."}

    results = []
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_dow = tomorrow.weekday()

    for product in products:
        # Check actual database order history for this product
        orders_data = OrderItem.objects.filter(product=product).values_list(
            'order__created_at__date', 'quantity'
        )

        # Build daily time series dataframe
        if len(orders_data) >= 14:
            df = pd.DataFrame(list(orders_data), columns=['date', 'quantity'])
            df = df.groupby('date').sum().reset_index()
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
        else:
            # Generate realistic synthetic 60-day baseline sales for initial academic demo
            base_demand = np.random.randint(15, 60)
            dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(60, 0, -1)]
            quantities = []
            for d in dates:
                dow = d.weekday()
                # Lunch surge on weekdays, lower on Sunday
                multiplier = 1.3 if dow in [1, 2, 3] else (0.5 if dow == 6 else 1.0)
                noise = np.random.normal(0, 3)
                q = max(5, int(base_demand * multiplier + noise))
                quantities.append(q)

            df = pd.DataFrame({'date': pd.to_datetime(dates), 'quantity': quantities})

        # Feature Engineering Pipeline
        df['dow'] = df['date'].dt.dayofweek
        df['is_weekend'] = df['dow'].apply(lambda x: 1 if x >= 5 else 0)
        df['lag_1'] = df['quantity'].shift(1).fillna(df['quantity'].mean())
        df['lag_7'] = df['quantity'].shift(7).fillna(df['quantity'].mean())
        df['rolling_7'] = df['quantity'].rolling(window=7, min_periods=1).mean()

        features = ['dow', 'is_weekend', 'lag_1', 'lag_7', 'rolling_7']
        X = df[features]
        y = df['quantity']

        # Train/Test Split (80% train, 20% test)
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        # Train Baseline Linear Regression
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        lr_preds = lr.predict(X_test)
        lr_mae = float(mean_absolute_error(y_test, lr_preds))

        # Train Random Forest Regressor
        rf = RandomForestRegressor(n_estimators=50, random_state=42)
        rf.fit(X_train, y_train)
        rf_preds = rf.predict(X_test)
        rf_mae = float(mean_absolute_error(y_test, rf_preds))
        rf_rmse = float(root_mean_squared_error(y_test, rf_preds))

        # Tomorrow's feature vector
        last_qty = float(df['quantity'].iloc[-1])
        lag_7_val = float(df['quantity'].iloc[-7] if len(df) >= 7 else last_qty)
        rolling_7_val = float(df['rolling_7'].iloc[-1])
        is_wknd = 1 if tomorrow_dow >= 5 else 0

        tomorrow_features = pd.DataFrame([{
            'dow': tomorrow_dow,
            'is_weekend': is_wknd,
            'lag_1': last_qty,
            'lag_7': lag_7_val,
            'rolling_7': rolling_7_val
        }])

        pred_qty = max(1, int(round(rf.predict(tomorrow_features)[0])))

        # Save to database
        forecast_obj, _ = DemandForecast.objects.update_or_create(
            product=product,
            forecast_date=tomorrow,
            model_name="RandomForestRegressor",
            defaults={
                'predicted_quantity': pred_qty,
                'mae_score': round(rf_mae, 2),
                'rmse_score': round(rf_rmse, 2)
            }
        )

        results.append({
            'product': product.name,
            'forecast_date': tomorrow.strftime('%Y-%m-%d'),
            'predicted_quantity': pred_qty,
            'mae': round(rf_mae, 2),
            'rmse': round(rf_rmse, 2),
            'baseline_lr_mae': round(lr_mae, 2)
        })

    return {
        "status": "success",
        "forecast_date": tomorrow.strftime('%d-%b-%Y'),
        "results": results
    }

