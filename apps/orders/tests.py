from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from apps.menu.models import Category, Product, TableQR
from apps.inventory.models import Ingredient, Recipe, StockTransaction, Notification
from apps.orders.models import Order, OrderItem, Payment
from apps.analytics.ml_service import train_and_forecast_demand

User = get_user_model()


class SmartCanteenWorkflowTests(TestCase):
    def setUp(self):
        # 1. Create Users
        self.admin_user = User.objects.create_user(
            username='test_admin', password='password123', role=User.Role.ADMIN, is_staff=True
        )
        self.kitchen_user = User.objects.create_user(
            username='test_chef', password='password123', role=User.Role.KITCHEN
        )
        self.student_user = User.objects.create_user(
            username='test_student', password='password123', role=User.Role.STUDENT
        )

        # 2. Category & Dish
        self.category = Category.objects.create(name='Snacks')
        self.samosa = Product.objects.create(
            category=self.category,
            name='Hot Samosa',
            price=Decimal('20.00'),
            preparation_time=5,
            is_available=True
        )

        # 3. Raw Ingredient & Recipe BOM
        self.potato = Ingredient.objects.create(
            name='Potatoes',
            unit=Ingredient.Unit.KILOGRAM,
            current_stock=Decimal('10.000'),
            minimum_threshold=Decimal('2.000'),
            unit_cost=Decimal('25.00')
        )
        self.recipe = Recipe.objects.create(
            product=self.samosa,
            ingredient=self.potato,
            quantity_required=Decimal('0.200') # 200g potatoes per samosa
        )

        self.client = Client()

    def test_student_order_and_recipe_stock_deduction(self):
        """
        End-to-End Test:
        1. Student logs in
        2. Adds 10x Samosas to Tray (Requires 10 * 0.2kg = 2.0kg Potatoes)
        3. Checkouts order
        4. Chef confirms order on KDS
        5. Verify Potatoes current_stock decrements from 10.0kg to 8.0kg
        6. Verify StockTransaction audit entry created
        """
        # Step 1: Login as student
        login_success = self.client.login(username='test_student', password='password123')
        self.assertTrue(login_success)

        # Step 2: Add to cart
        self.client.get(reverse('orders:add_to_cart', args=[self.samosa.id]))
        session = self.client.session
        session['cart'][str(self.samosa.id)]['quantity'] = 10
        session.save()

        # Step 3: Checkout
        response = self.client.post(reverse('orders:checkout'), {
            'payment_mode': Payment.Mode.UPI_MOCK,
            'notes': 'Extra crispy please'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        order = Order.objects.get(user=self.student_user)
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(order.total_amount, Decimal('200.00')) # 10 * 20.00
        self.assertEqual(self.potato.current_stock, Decimal('10.000')) # Not deducted until confirmed

        # Step 4: Login as kitchen chef and confirm order
        self.client.logout()
        self.client.login(username='test_chef', password='password123')

        response = self.client.post(
            reverse('orders:update_order_status', args=[order.id]),
            {'status': Order.Status.CONFIRMED},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Step 5: Verify Order Status & Atomic Recipe Stock Decrement
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CONFIRMED)

        self.potato.refresh_from_db()
        # 10.000 - (10 * 0.200) = 8.000 kg
        self.assertEqual(self.potato.current_stock, Decimal('8.000'))

        # Step 6: Verify Audit Trail
        txn = StockTransaction.objects.filter(reference_order=order).first()
        self.assertIsNotNone(txn)
        self.assertEqual(txn.quantity, Decimal('-2.000'))
        self.assertEqual(txn.transaction_type, StockTransaction.TransactionType.ORDER_DEDUCTION)

    def test_low_stock_threshold_notification_trigger(self):
        """
        Verify that when stock falls below safety threshold, an automated in-app notification is fired.
        """
        # Set potato current_stock near threshold
        self.potato.current_stock = Decimal('2.100')
        self.potato.save()

        order = Order.objects.create(
            user=self.student_user,
            total_amount=Decimal('40.00'),
            status=Order.Status.PENDING
        )
        OrderItem.objects.create(
            order=order, product=self.samosa, quantity=2, unit_price=Decimal('20.00')
        )

        self.client.login(username='test_chef', password='password123')
        self.client.post(reverse('orders:update_order_status', args=[order.id]), {'status': Order.Status.CONFIRMED})

        self.potato.refresh_from_db()
        # 2.100 - (2 * 0.200) = 1.700 kg, which is <= 2.000 kg threshold!
        self.assertEqual(self.potato.current_stock, Decimal('1.700'))
        self.assertTrue(self.potato.is_low_stock)

        # Verify Notification generated
        notification = Notification.objects.filter(title__icontains="Low Stock Alert").first()
        self.assertIsNotNone(notification)

    def test_ml_demand_forecasting_pipeline(self):
        """
        Verify that Scikit-Learn regression pipeline executes and generates predictions.
        """
        result = train_and_forecast_demand()
        self.assertEqual(result.get('status'), 'success')
        self.assertTrue(len(result.get('results')) > 0)
