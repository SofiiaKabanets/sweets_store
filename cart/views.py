import random
import stripe.error
from .models import Cart, CartItem
from shop.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal
from vouchers.forms import VoucherApplyForm
from django.utils import timezone
from order.models import Order, OrderItem
from cart.models import UserActivity


def cart(request):
    
    cart = None
    cartitems = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
    else:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
    
    context = {"cart":cart, "items":cartitems}
    return render(request, "cart.html", context)



def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("index")



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        UserActivity.objects.create(
        user=request.user,
        item=product,
        timestamp=timezone.now(),
        rating = 1
        )
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    if 'voucher_id' in request.session:
        del request.session['voucher_id']

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if (cart_item.quantity < cart_item.product.stock):
            cart_item.quantity +=1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1,cart=cart)
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    voucher_form = VoucherApplyForm(request.POST or None)
    voucher_id = request.session.get('voucher_id')
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    
    if voucher_id:
        try:
            voucher = Voucher.objects.get(id=voucher_id)
            if voucher.active and voucher.valid_from <= timezone.now() <= voucher.valid_to:
                total -= (total * (voucher.discount / Decimal('100')))
        except Voucher.DoesNotExist:
            pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Online Shop - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    recommendations = []
    if request.user.is_authenticated:
        latest_activities = {}
        user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
        for activity in user_activities:
            if activity.item.id not in latest_activities:
                latest_activities[activity.item.id] = activity

        latest_product_ids = [activity.item.id for activity in latest_activities.values()]

        latest_product_ids = set(latest_product_ids) - set(CartItem.objects.filter(cart=cart).values_list('product__id', flat=True))

        max_recommendations = min(len(latest_product_ids), 3)

        random_recommendations = random.sample(list(latest_product_ids), max_recommendations)

        recommendations = Product.objects.filter(id__in=random_recommendations)

   

    if request.method =='POST':
        print(request.POST)
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingcity = request.POST['stripeShippingAddressCity']
            shippingCountry = request.POST['stripeShippingAddressCountryCode'] 

            customer = stripe.Customer.create(email=email, source=token)

            stripe.Charge.create(amount=stripe_total,
                                 currency="eur", 
                                 description=description,
                                 customer=customer.id)
            
            try:
                order_details = Order.objects.create(
                    token = token,
                    total = total,
                    emailAddress = email,
                    billingName = billingName,
                    billingAddress1 = billingAddress1,
                    billingCity = billingcity,
                    billingCountry = billingCountry,
                    shippingName = shippingName,
                    shippingAddress1 = shippingAddress1,
                    shippingCity = shippingcity,
                    shippingCountry = shippingCountry
                    )
                order_details.save()

                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        product = order_item.product,
                        quantity = order_item.quantity,
                        price = order_item.product.price,
                        order = order_details)
                    oi.save()
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock -
                    order_item.quantity)
                    products.save()
                    order_item.delete()

                    print('The order has been created')
                return redirect ('order:thanks', order_details.id) 


            except ObjectDoesNotExist:
                pass


        except stripe.error.CardError as e:
            return e    

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'data_key': data_key,
        'stripe_total': stripe_total,
        'description': description,
        'voucher_form': voucher_form,
        'recommendations': recommendations
    })

    
def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("cart:cart_detail")


def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart:cart_detail")