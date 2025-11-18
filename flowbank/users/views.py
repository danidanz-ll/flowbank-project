from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from users.backends import CPFBackend


# 🔹 Registro de novo usuário
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # cria o usuário
            login(request, user, backend='users.backends.CPFBackend')  # informa o backend
            messages.success(request, "Conta criada com sucesso!")
            return redirect('accounts:home')
        else:
            messages.error(request, "Verifique os campos e tente novamente.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# 🔹 Login via CPF
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='users.backends.CPFBackend')
            return redirect('accounts:home')
        else:
            print("❌ Erros do formulário:", form.errors.as_json())
            messages.error(request, "CPF ou senha incorretos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect('home')
