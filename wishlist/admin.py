from django.contrib import admin
from .models import Wishlist,WishlistItem, ShareWishlist

admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(ShareWishlist)
