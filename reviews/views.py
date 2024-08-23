from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Review
from shop.models import Product
from django.contrib.auth.decorators import login_required
import uuid


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        review = Review.objects.create(product=product, user=user, text=text, rating=rating)
        return redirect('shop:product-detail', pk=product_id)

    else:
        return render(request, 'reviews/add_review.html', {'product': product})