from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product
from .models import Wishlist, WishlistItem, ShareWishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages


@login_required
def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user=request.user
    wishlist, created= Wishlist.objects.get_or_create(wishlist_id=user.id)
    # created = Wishlist.objects.get_or_create(wishlist_id=user.id)
    if created:
        pass
    try:
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
        wishlist_item.quantity +=1
        wishlist_item.save()
    except WishlistItem.DoesNotExist:
        WishlistItem.objects.create(product=product, quantity=1, wishlist=wishlist)
    return redirect('wishlist:wishlist_detail')


@login_required
def wishlist_detail(request):
    user=request.user
    try:
        wishlist = Wishlist.objects.filter(wishlist_id=user.id).first()
        wishlist_items=WishlistItem.objects.filter(wishlist=wishlist, active=True)
    except Wishlist.DoesNotExist:
        wishlist_items=[]

    return render(request, "wishlist.html", {'wishlist_items': wishlist_items})


#remove quantity

@login_required
def wishlist_remove(request, product_id):
    wishlist= Wishlist.objects.get(wishlist_id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    if wishlist_item.quantity > 1: 
        wishlist_item.quantity -= 1
        wishlist_item.save()
    else: 
        wishlist_item.delete()
    return redirect('wishlist:wishlist_detail') 


#delete

@login_required
def full_remove(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    return redirect('wishlist:wishlist_detail') 



@login_required
def wishlist_search(request):
    user = request.user
    query = request.GET.get('q')
    wishlist = Wishlist.objects.filter(wishlist_id=user.id).first()
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, active=True)
    search_results = None
    if query:
        search_results = wishlist_items.filter(
            Q(product__name__icontains=query) |
            Q(product__description__icontains=query)
        )
    
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items,'search_results': search_results})


@login_required
def share_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, wishlist_id=wishlist_id)

    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        message = request.POST.get('message', '')

        shared_wishlist = ShareWishlist.objects.create(
            wishlist=wishlist,
            sender_email=request.user.email,
            recipient_email=recipient_email,
            message=message
        )

        subject = 'Take a look at my wishlist'
        email_content = render_to_string('shared_wishlist.html', {
            'shared_wishlist': shared_wishlist,
            'site_url': request.build_absolute_uri('/')
        })
        try:
            send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [recipient_email])
            messages.success(request, "Wishlist shared successfully")
        except Exception as e:
            messages.error(request, f"Wishlist was not shared successfully: {e}")

        return redirect('wishlist:wishlist_detail')


    else:
        message.warning(request, "Feature not yet available")      
        return redirect('wishlist:wishlist_detail')
    
        # return render(request, 'wishlist/shared_wishlist.html', {'wishlist': wishlist, 'success_message': 'Yay wishlist was shared successfully'})
    
    
