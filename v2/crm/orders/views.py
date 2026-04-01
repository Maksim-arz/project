from django.shortcuts import render
from .models import Order

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/orders_list.html', {'orders': orders})