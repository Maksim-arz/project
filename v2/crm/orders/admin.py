from django.contrib import admin
from django.utils.html import format_html
from .models import MenuItem, Order, OrderItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'image_preview']
    list_filter  = ['category', 'is_available']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Фото'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'client', 'status', 'created_at']
    list_filter  = ['status']
    inlines      = [OrderItemInline]
