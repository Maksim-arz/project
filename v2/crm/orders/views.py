from django.core.mail import send_mail
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from accounts.views import manager_required
from .models import MenuItem, Order, OrderItem

NOTIFY_STATUSES = {
    Order.Status.IN_WORK:   'В работе',
    Order.Status.COMPLETED: 'Завершён',
}


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
    base_qs = Order.objects.select_related('client').prefetch_related('items__menu_item')
    active = (
        base_qs
        .filter(status__in=[Order.Status.IN_WORK, Order.Status.NEW])
        .annotate(status_order=Case(
            When(status=Order.Status.IN_WORK, then=Value(0)),
            When(status=Order.Status.NEW, then=Value(1)),
            output_field=IntegerField(),
        ))
        .order_by('status_order', '-created_at')
    )
    history = base_qs.filter(
        status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]
    ).order_by('-created_at')
    return render(request, 'orders/manager_orders.html', {
        'active': active,
        'history': history,
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
            if new_status in NOTIFY_STATUSES:
                send_mail(
                    subject=f'Статус заказа #{order.pk} изменён',
                    message=f'Ваш заказ #{order.pk} «{NOTIFY_STATUSES[new_status]}».',
                    from_email=None,
                    recipient_list=[order.client.email],
                    fail_silently=True,
                )
    return redirect('manager_orders')
