from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def trade_edit(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_trade_edit.html', {'current_user': current_user})
    else:
        return render(request, 'user_log_trade_edit.html', {'current_user': current_user})


@login_required
def user_log(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_user_log.html', {'current_user': current_user})


@login_required
def auto(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_auto.html', {'current_user': current_user})


@login_required
def cross_log(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_cross.html', {'current_user': current_user})


@login_required
def rejection_log(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_rejection.html', {'current_user': current_user})
    else:
        return render(request, 'user_log_rejection.html', {'current_user': current_user})
