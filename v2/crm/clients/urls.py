from django.urls import path
from . import views

urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('add/', views.client_add, name='client_add'),
    path('<int:pk>/delete/', views.client_delete, name='client_delete'),
]