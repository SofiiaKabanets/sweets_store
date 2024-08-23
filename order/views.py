from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse



def thanks(request, order_id):
 if order_id:
    customer_order = get_object_or_404(Order, id=order_id)
 return render(request, 'thanks.html',{'customer_order': customer_order}) 



class orderHistory(LoginRequiredMixin, View):
    def get (self, request):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order_details = Order.objects.filter(emailAddress=email)
        return render(request, 'order/orders_list.html', {'order_details': order_details})


class orderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order = Order.objects.get(id=order_id, emailAddress=email)
            order_items = OrderItem.objects.filter(order=order)
            

        return render(request, 'order/order_detail.html', {'order': order, 'order_items': order_items})
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.cancel_order() 
        return HttpResponseRedirect(reverse('order:order_detail', args=[order_id]))
