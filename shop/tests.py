from django.test import TestCase
from .models import Category, Product


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Doughnuts',
            description='variety of doughnuts'
        )
        self.product = Product.objects.create(
            name='glazed doughnut',
            description='doughnut glazed with sugar',
            category=self.category,
            price=7,
            stock=1,
            available=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'glazed doughnut')
        self.assertEqual(self.product.description, 'doughnut glazed with sugar')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 7)
        self.assertEqual(self.product.stock, 1)
        self.assertTrue(self.product.available)

    def test_product_str_method(self):
        self.assertEqual(str(self.product), 'glazed doughnut')

    def test_product_deletion(self):
        self.product.delete()
        deleted_product = Product.objects.filter(name='glazed doughnut').first()
        self.assertIsNone(deleted_product)
        category_exists = Category.objects.filter(name='Doughnuts').exists()
        self.assertTrue(category_exists)


    def test_product_str_method(self):
        self.assertEqual(str(self.product), 'glazed doughnut')    


