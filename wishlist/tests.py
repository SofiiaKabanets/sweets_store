from django.test import TestCase
from shop.models import Product, Category
from wishlist.models import Wishlist, WishlistItem
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import Client
from accounts.models import CustomUser
from django.utils.http import urlencode
import os



class WishlistViewTests(TestCase):
    def setUp(self):


        user = User.objects.create(username='testuser')
        user.set_password('test12345678')
        user.save()

        c = Client()
        logged_in = c.login(username='testuser', password='12345')

        # User=get_user_model()
        # self.user = User.objects.create_user(username='testuser', password='test12345678')
        # self.client.login(username='testuser', password='test12345678')

        self.c = Category.objects.create(name='Cake')
        self.product = Product.objects.create(name='cake',
            price=80.0,
            stock=2,
            category=self.c,
        )

        self.wishlist= Wishlist.objects.get(wishlist_id=logged_in.session.session_key)
        self.wishlist_item = WishlistItem.objects.create(
            product=self.product,
            wishlist=self.wishlist,
            quantity=1,
            active=True
        )

        

    def test_add_wishlist(self):

        search_url=reverse('wishlist:add_wishlist', args=[self.product.id])
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, 302)  
        
        wishlist_item = WishlistItem.objects.get(product=self.product, wishlist=self.wishlist)
        self.assertEqual(wishlist_item.quantity, 1)


    def test_add_wishlist_quantity(self):
        response = self.client.get(reverse('wishlist:add_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  
        wishlist = Wishlist.objects.get(wishlist_id=self.client.session.session_key)
        wishlist_item = WishlistItem.objects.get(product=self.product, wishlist=wishlist)
        self.assertEqual(wishlist_item.quantity, 1)


    def test_lessen_wishlist_quantity(self):
        response = self.client.get(reverse('wishlist:wishlist_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  
        wishlist = Wishlist.objects.get(wishlist_id=self.client.session.session_key)
        wishlist_item = WishlistItem.objects.get(product=self.product, wishlist=wishlist)
        self.assertEqual(wishlist_item.quantity, 0)


    def test_wishlist_full_remove(self):
        request = self.client.request().wsgi_request
        request.session = self.client.session
        request.session.save()

        request.session['wishlist_id'] = self._wishlist_id(request)
        response = self.client.post(reverse('wishlist:full_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(WishlistItem.DoesNotExist):
            WishlistItem.objects.get(id=WishlistItem.id)

    def test_wishlist_search(self):
        search_url=reverse('wishlist:wishlist_search')
        in_query = urlencode({'q':'cake'})
        response = self.client.get(f'{search_url}?{in_query}')
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.product1.name, response.content.decode())










