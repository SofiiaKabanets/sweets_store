from django.test import TestCase
from search.models import Product, Category
from shop.models import Product, Category
from django.urls import reverse
from django.utils.http import urlencode
import os



# Create your tests here.

class SearchTest(TestCase):
    def setUp(self):
        self.c = Category.objects.create(name='Cake')

        media_dir = os.path.join(os.path.dirname(__file__),'media')
        image_path = os.path.join(media_dir,'images/logo1.jpng')

        self.product1 = Product.objects.create(
            name='cake',
            price=80.0,
            stock=2,
            category=self.c,
            image=image_path
        )

        self.product2 = Product.objects.create(
            name='cake2',
            price=120.0,
            stock=2,
            category=self.c,
            image=image_path
        )

    def test_search_success(self):
        #assign
        search_url=reverse('search:searchResult')
        in_query = urlencode({'q':'cake'})
        result = self.client.get(f'{search_url}?{in_query}')

        #assert
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.product1.name, result.content.decode())


    def test_search_fail(self):
        #assign
        search_url=reverse('search:searchResult')
        in_query = urlencode({'q':'zzz'})
        result = self.client.get(f'{search_url}?{in_query}')

        #assert
        self.assertEqual(result.status_code, 200)
        self.assertIn('zzz', result.content.decode())

    def test_search_min(self):
        min_price=90
        search_url=reverse('search:searchResult')
        result = self.client.get(search_url+f'?min_price={min_price}')

        self.assertContains(result, self.product1.name)

    def test_search_max(self):
        max_price=120
        search_url=reverse('search:searchResult')
        result = self.client.get(search_url+f'?max_price={max_price}')

        self.assertContains(result, self.product2.name)

    def test_search_min_max(self):
        min_price=90
        max_price=120
        search_url=reverse('search:searchResult')
        result = self.client.get(search_url+f'?min_price={min_price}&max_price={max_price}')

        self.assertContains(result, self.product2.name)

    def test_search_min_max_category(self):
        min_price=90
        max_price=120
        category=self.c.id
        search_url=reverse('search:searchResult')
        result = self.client.get(search_url+f'?min_price={min_price}&max_price={max_price}&category={category}')

        self.assertContains(result, self.product2.name)

                                 
                                 
        

