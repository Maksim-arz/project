from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('add/', views.order_add, name='order_add'),
    path('<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('client/<int:pk>/active/', views.client_active_orders, name='client_active_orders'),
    path('client/<int:pk>/history/', views.client_order_history, name='client_order_history'),
]