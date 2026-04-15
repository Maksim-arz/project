from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('manager/orders/', views.manager_orders, name='manager_orders'),
    path('my-orders/<int:pk>/cancel/', views.client_cancel_order, name='client_cancel_order'),
    path('manager/orders/<int:pk>/status/', views.manager_order_status, name='manager_order_status'),
]
