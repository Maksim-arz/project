from django.conf import settings
from django.db import models


class MenuItem(models.Model):
    class Category(models.TextChoices):
        FOOD  = 'food',  'Еда'
        DRINK = 'drink', 'Напиток'

    name         = models.CharField(max_length=100)
    description  = models.CharField(max_length=200, blank=True)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    category     = models.CharField(max_length=10, choices=Category.choices)
    is_available = models.BooleanField(default=True)
    image        = models.ImageField(upload_to='menu/', blank=True, null=True)

    class Meta:
        verbose_name = 'Позиция меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        NEW       = 'new',       'Новый'
        IN_WORK   = 'in_work',   'В работе'
        COMPLETED = 'completed', 'Завершён'
        CANCELLED = 'cancelled', 'Отменён'

    client     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.client}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity  = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.menu_item.name} x{self.quantity}'

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity
