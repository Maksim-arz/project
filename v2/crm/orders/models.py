from django.db import models
from clients.models import Client

class Order(models.Model):
    class Priority(models.TextChoices):
        LOW = "Низкий"
        MEDIUM = "Средний"
        HIGH = "Высокий"
    
    class Status(models.TextChoices):
        NEW = "Новый"
        IN_WORK = "В работе"
        COMPLETED = "Завершен"
        CANCELLED = "Отменен"
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    description = models.CharField(max_length=500)
    price = models.FloatField()
    priority = models.CharField(max_length=15, choices=Priority.choices)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NEW)
    deadline = models.DateField()

    def __str__(self):
        return f"Заказ #{self.pk} - {self.client}"