from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manager/clients/', views.manager_clients, name='manager_clients'),
    path('manager/clients/create/', views.manager_client_create, name='manager_client_create'),
    path('manager/clients/<int:pk>/edit/', views.manager_client_edit, name='manager_client_edit'),
    path('manager/clients/<int:pk>/delete/', views.manager_client_delete, name='manager_client_delete'),
]