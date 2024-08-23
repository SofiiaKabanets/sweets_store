from django.db import models
from shop.models import Product
from accounts.models import CustomUser
import uuid


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    

    class Meta:
        db_table = 'Wishlist'
        ordering = ['date_added']

    def __str__(self):
        return self.wishlist_id
    
class WishlistItem(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'WishlistItem'
    
    def __str__(self):
        return "{self.product.name} - {self.quantity}"
    
class ShareWishlist(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    wishlist_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    sender_email = models.EmailField()
    recipient_email = models.EmailField()
    message = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ShareWishlist'
