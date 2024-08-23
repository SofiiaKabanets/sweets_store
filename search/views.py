from .models import Product, Category
from django.shortcuts import render
from shop.models import Product, Category
from django.views.generic import ListView, DetailView
from django.db.models import Q



class SearchResultListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        min_price=self.request.GET.get('min_price')
        max_price=self.request.GET.get('max_price')
        category_id=self.request.GET.get('category')
         
        queryset=Product.objects.all()
        
        if query:
             queryset = queryset.filter(Q(name__icontains=query))

        if min_price !='' and min_price is not None:
            queryset=queryset.filter(price__gte=min_price)
        if max_price !='' and max_price is not None:
            queryset=queryset.filter(price__lte=max_price)

        if category_id:
            queryset=queryset.filter(category_id=category_id)

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['categories']=Category.objects.all()

        return context
    

    
