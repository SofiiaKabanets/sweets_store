from shop.models import Product
from accounts.models import CustomUser
from django.db import models

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'CartItem'
    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.product 
    
class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities', blank=True,null=True )
    item = models.ForeignKey(Product, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "User_Activities"

    def __str__(self):
        return f"{self.user.username} - {self.item} - {self.timestamp}"
