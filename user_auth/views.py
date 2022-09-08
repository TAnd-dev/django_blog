from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user_auth.forms import UserRegisterForm, UserLoginForm


def user_reg(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('admin')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'user_auth/auth.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = UserLoginForm()
    return render(request, 'user_auth/auth.html', {'form': form})
