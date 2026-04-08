from django.shortcuts import render, redirect, get_object_or_404
from .models import Client

def clients_list(request):
    clients = Client.objects.all()
    return render(request, "clients/clients_list.html", {'clients': clients})

def client_add(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        if name:
            Client.objects.create(name=name, phone=phone, email=email)
            return redirect("clients_list")
    return render(request, "clients/client_add.html")

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        return redirect("clients_list")
    return render(request, "clients/client_confirm_delete.html", {'client': client})