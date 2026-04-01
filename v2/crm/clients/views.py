from django.shortcuts import render
from .models import Client

def clients_list(request):
    clients = Client.objects.all()
    return render(request, "clients/clients_list.html", {'clients': clients})