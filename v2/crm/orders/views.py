from django.shortcuts import get_object_or_404, redirect, render

from accounts.views import manager_required
from .models import MenuItem, Order, OrderItem


def _client_required(request):
    # Возвращает redirect если пользователь не клиент, иначе None.
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_client:
        return redirect('dashboard')
    return None


def menu_view(request):
    guard = _client_required(request)
    if guard:
        return guard

    if request.method == 'POST':
        item_ids = request.POST.getlist('items')
        if item_ids:
            order = Order.objects.create(client=request.user)
            for item_id in item_ids:
                try:
                    qty = max(1, int(request.POST.get(f'quantity_{item_id}', 1)))
                except ValueError:
                    qty = 1
                OrderItem.objects.create(order=order, menu_item_id=item_id, quantity=qty)
            return redirect('my_orders')

    food   = MenuItem.objects.filter(is_available=True, category=MenuItem.Category.FOOD)
    drinks = MenuItem.objects.filter(is_available=True, category=MenuItem.Category.DRINK)
    return render(request, 'orders/menu.html', {'food': food, 'drinks': drinks})


def my_orders(request):
    guard = _client_required(request)
    if guard:
        return guard

    active = (
        request.user.orders
        .filter(status__in=[Order.Status.NEW, Order.Status.IN_WORK])
        .order_by('-created_at')
        .prefetch_related('items__menu_item')
    )
    history = (
        request.user.orders
        .filter(status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED])
        .order_by('-created_at')
        .prefetch_related('items__menu_item')
    )
    return render(request, 'orders/my_orders.html', {'active': active, 'history': history})


@manager_required
def manager_orders(request):
    orders = (
        Order.objects
        .all()
        .order_by('-created_at')
        .select_related('client')
        .prefetch_related('items__menu_item')
    )
    return render(request, 'orders/manager_orders.html', {
        'orders': orders,
        'statuses': Order.Status.choices,
    })


def client_cancel_order(request, pk):
    guard = _client_required(request)
    if guard:
        return guard

    order = get_object_or_404(Order, pk=pk, client=request.user)
    if request.method == 'POST' and order.status == Order.Status.NEW:
        order.status = Order.Status.CANCELLED
        order.save()
    return redirect('my_orders')


@manager_required
def manager_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save()
    return redirect('manager_orders')
