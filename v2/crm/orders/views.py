from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from clients.models import Client

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/orders_list.html', {'orders': orders})

def order_add(request):
    clients = Client.objects.all()
    if request.method == "POST":
        client_id = request.POST.get("client_id")
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "0")
        priority = request.POST.get("priority")
        deadline = request.POST.get("deadline")
        if client_id and description and deadline:
            client = get_object_or_404(Client, pk=client_id)
            Order.objects.create(
                client=client,
                description=description,
                price=float(price),
                priority=priority,
                deadline=deadline,
            )
            return redirect("orders_list")
    return render(request, 'orders/order_add.html', {
        'clients': clients,
        'priorities': Order.Priority.choices,
    })

def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        description = request.POST.get("description", "").strip()
        if status:
            order.status = status
        if priority:
            order.priority = priority
        if description:
            order.description = description
        order.save()
        return redirect("orders_list")
    return render(request, 'orders/order_update_status.html', {
        'order': order,
        'statuses': Order.Status.choices,
        'priorities': Order.Priority.choices,
    })

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("orders_list")
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

def client_active_orders(request, pk):
    client = get_object_or_404(Client, pk=pk)
    orders = client.orders.filter(
        status__in=[Order.Status.NEW, Order.Status.IN_WORK]
    ).order_by('-price')
    return render(request, 'orders/client_active_orders.html', {
        'client': client,
        'orders': orders,
    })

def client_order_history(request, pk):
    client = get_object_or_404(Client, pk=pk)
    orders = client.orders.filter(
        status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]
    )
    return render(request, 'orders/client_order_history.html', {
        'client': client,
        'orders': orders,
    })