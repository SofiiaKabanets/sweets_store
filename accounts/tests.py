from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class SignUpViewTest(TestCase):
    def test_signup_success(self):
        response = self.client.post(reverse('signup'), {'username': 'test_user', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('accounts:login'))  

    def test_signup_failure(self):
        response = self.client.post(reverse('signup'), {'username': '', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 200)  

class ProfilePageViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_page_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)  

class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_update_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('profile_update', kwargs={'pk': self.profile.pk}), {'fname': 'Updated Name'})
        self.assertEqual(response.status_code, 302)


class CustomLoginViewTest(TestCase):
    def test_login_view(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  

class CustomLogoutViewTest(TestCase):
    def test_logout_view(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('accounts:login')) 
