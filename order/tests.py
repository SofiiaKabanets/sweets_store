from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from order.models import Order, OrderItem
from shop.models import Product, Category

CustomUser = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        category = Category.objects.create(name='Test Category')

        self.product = Product.objects.create(
            name='Test Product',
            price=50,
            stock=10,
            category=category
        )

        self.order = Order.objects.create(
            total=100,
            emailAddress='test@example.com',
            billingName='Test User',
            billingAddress1='Test Address',
            billingCity='Test City',
            billingPostcode='12345',
            billingCountry='Test Country',
            shippingName='Test User',
            shippingAddress1='Test Address',
            shippingCity='Test City',
            shippingPostcode='12345',
            shippingCountry='Test Country'
        )

        self.order_item = OrderItem.objects.create(
            product=self.product,
            quantity=2,
            price=50,
            order=self.order
        )

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(self.order.status, 'Pending')
        self.assertEqual(self.order.total, 100)

    def test_order_item_creation(self):
        self.assertTrue(isinstance(self.order_item, OrderItem))
        self.assertEqual(self.order_item.sub_total(), 100)


class OrderViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        category = Category.objects.create(name='Test Category')

        self.product = Product.objects.create(
            name='Test Product',
            price=50,
            stock=10,
            category=category
        )

        self.order = Order.objects.create(
            total=100,
            emailAddress='test@example.com',
            billingName='Test User',
            billingAddress1='Test Address',
            billingCity='Test City',
            billingPostcode='12345',
            billingCountry='Test Country',
            shippingName='Test User',
            shippingAddress1='Test Address',
            shippingCity='Test City',
            shippingPostcode='12345',
            shippingCountry='Test Country',
            status='Pending'
        )

        self.order_item = OrderItem.objects.create(
            product=self.product,
            quantity=2,
            price=50,
            order=self.order
        )

    def test_order_history_view(self):
        response = self.client.get(reverse('order:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/orders_list.html')

    def test_cancel_order_view(self):
        response = self.client.post(reverse('order:order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get(id=self.order.id).status, 'Canceled')
