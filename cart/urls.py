from django.urls import path
from .views import  add_cart, cart_detail, confirm_payment, cart_remove, full_remove

app_name = 'cart'

urlpatterns = [
    path('add/<uuid:product_id>/', add_cart, name='add_cart'),
    path("confirm_payment/<str:pk>", confirm_payment, name="add"),
    path('remove/<uuid:product_id>/', cart_remove, name='cart_remove'),
    path('', cart_detail, name='cart_detail'),
    path('full_remove/<uuid:product_id>/',full_remove,name='full_remove'),
]