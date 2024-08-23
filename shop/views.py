
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Category
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from cart.models import UserActivity 
from django.utils import timezone

class ProductListView(ListView):
    model=Product
    template_name='home.html'
    context_object_name="all_products_list"
    
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = Product.objects.filter(category=category, stock__gt=0)
        else:
            queryset = Product.objects.filter(stock__gt=0)
            
        return queryset
    


class ProductDetailView(DetailView):
    model=Product
    template_name='product_detail.html'

class ProductCreateView(CreateView):
    model=Product
    template_name='product_new.html'

class ProductUpdateView(UpdateView):
    model=Product
    template_name='product_edit.html'
    fields=['description', 'price', 'stock', 'available']  
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model=Product
    template_name='product_delete.html'
    success_url=reverse_lazy

class CategoryListView(ListView):
    model=Category
    template_name='category.html'
    context_object_name = "categories_list_products"
    paginate_by = 6 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_list_products = self.get_queryset()
        context['products'] = self.get_queryset()# Retrieve the queryset
        paginator = Paginator(categories_list_products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        category_id = self.kwargs.get('category_id')
        context['category_id'] = category_id
        context['categories'] = Category.objects.all()
        context['categories_list_products'] = page_obj  # Assign paginated queryset to context
        
        if category_id:
            context['current_category'] = get_object_or_404(Category, id=category_id)

        return context
    

    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = Product.objects.filter(category=category, stock__gt=0)
        else:
            queryset = Product.objects.filter(stock__gt=0)

        return queryset  
        
    

    
def ProductDetail(request, pk):

    product = get_object_or_404(Product,id=pk)
    if request.user.is_authenticated:
        UserActivity.objects.create(
        user=request.user,
        item=product,
        timestamp=timezone.now(),
        rating = 1
        )
    return render(request, 'product.html', {'product':product})

    

    
