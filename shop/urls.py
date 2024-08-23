from django.urls import path, include
from .views import ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductDetail, CategoryListView
from wishlist.views import wishlist_detail, add_wishlist
from . import views

app_name = 'shop'

urlpatterns = [
    path('', CategoryListView.as_view(), name='product-list'),
    path('product/<uuid:pk>/', ProductDetail, name='all_products'),
    path('product/retail/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<uuid:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('product/<uuid:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('orders/', include('order.urls')),
    path('wishlist/', wishlist_detail, name='wishlist_detail'),
    path('wishlist/add/<uuid:product_id>/', add_wishlist, name='add_wishlist'),
    path('<uuid:category_id>/', CategoryListView.as_view(), name="products_by_category"),
    path('product/all/<uuid:pk>/', ProductDetail, name='all_products'),
    path('product/retail/<uuid:pk>/', ProductDetailView.as_view(), name='retail-product-detail'),
    path('product/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('', ProductListView.as_view(), name='all_products'),
]
