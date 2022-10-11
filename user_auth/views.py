from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user_auth.forms import UserRegisterForm, UserLoginForm


def user_reg(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            message = 'Вы успешно зарегестрировались. Для большего функционала привяжите почту в настройках профиля'
            messages.success(request, message)
            login(request, user)
            return redirect('blog')
        else:
            message = 'Ошибка регистрации'
            messages.error(request, message)
    else:
        form = UserRegisterForm()
    return render(request, 'user_auth/auth.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = UserLoginForm()
    return render(request, 'user_auth/auth.html', {'form': form})
