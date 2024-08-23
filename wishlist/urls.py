from django.urls import path
from . import views

app_name='wishlist'
urlpatterns = [
    path('add/<uuid:product_id>/', views.add_wishlist, name='add_wishlist'),
    path('', views.wishlist_detail, name='wishlist_detail'),
    path('remove/<uuid:product_id>/', views.wishlist_remove, name='wishlist_remove'),
    path('full_remove/<uuid:product_id>/', views.full_remove, name='full_remove'),
    path('search/', views.wishlist_search, name='wishlist_search'),
    # path('wishlist_email/<uuid:wishlist_id>', views.wishlist_email, name='wishlist_email'),
]

