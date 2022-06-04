from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import stack
# import db.session


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            if stack.objects.filter(username=request.user).exists():
                return redirect('/dashboard')
            else:
                print("New stack created for" + request.user.username)
                newstack = stack(username=request.user, stocks={"data": []})
                newstack.save()
                print(newstack)
                return redirect('/dashboard')
        else:
            messages.success(request, ('Error logging in - please try again.'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('accounts:login_user')


@login_required
def cash_ledge(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_ledge.html', {'current_user': current_user})


@login_required
def cash_entry(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_entry.html', {'current_user': current_user})


@login_required
def jv(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_jv.html', {'current_user': current_user})


@login_required
def jv_broker(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_jv_broker.html', {'current_user': current_user})


@login_required
def jv_broker_delete(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_jv_broker_delete.html', {'current_user': current_user})


@login_required
def deposit_entry(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_deposit.html', {'current_user': current_user})


@login_required
def valan(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_valan.html', {'current_user': current_user})
