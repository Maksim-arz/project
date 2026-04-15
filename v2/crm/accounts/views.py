from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm, LoginForm, RegisterForm
from .models import User



def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_manager:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        form.add_error(None, 'Неверный email или пароль')
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.role = User.Role.CLIENT
        user.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_manager:
        return redirect('manager_clients')
    return render(request, 'accounts/client_dashboard.html')



@manager_required
def manager_clients(request):
    clients = User.objects.filter(role=User.Role.CLIENT).order_by('email')
    return render(request, 'accounts/manager_clients.html', {'clients': clients})


@manager_required
def manager_client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.role = User.Role.CLIENT
        user.save()
        return redirect('manager_clients')
    return render(request, 'accounts/manager_client_form.html', {
        'form': form,
        'title': 'Создать клиента',
    })


@manager_required
def manager_client_delete(request, pk):
    client = get_object_or_404(User, pk=pk, role=User.Role.CLIENT)
    if request.method == 'POST':
        client.delete()
        return redirect('manager_clients')
    return render(request, 'accounts/manager_client_confirm_delete.html', {'client': client})


@manager_required
def manager_client_edit(request, pk):
    client = get_object_or_404(User, pk=pk, role=User.Role.CLIENT)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        return redirect('manager_clients')
    return render(request, 'accounts/manager_client_form.html', {
        'form': form,
        'title': 'Редактировать клиента',
        'client': client,
    })