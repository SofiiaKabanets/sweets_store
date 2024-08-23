from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Review
from shop.models import Product, Category


class ReviewListViewTest(TestCase):
    def test_review_list_view(self):
        response = self.client.get(reverse('reviews:review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_list.html')


class AddReviewViewTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='testuser', password='password')
        category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.0, stock=10, category=category)

    def test_add_review_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('reviews:add_review', kwargs={'product_id': self.product.id}), 
                                    {'text': 'Test review', 'rating': 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_add_review_view_unauthenticated(self):
        response = self.client.post(reverse('reviews:add_review', kwargs={'product_id': self.product.id}), 
                                    {'text': 'Test review', 'rating': 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0) #still have problem with urls(check later)
