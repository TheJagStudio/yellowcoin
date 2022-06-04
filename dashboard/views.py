from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_trades.html', {'current_user': current_user})
    else:
        return render(request, 'user_dashboard_trades.html', {'current_user': current_user})


@login_required
def trade_entry(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_trade_entry.html', {'current_user': current_user})


@login_required
def exected_order(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_executed_orders.html', {'current_user': current_user})


@login_required
def running_orders(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_running_orders.html', {'current_user': current_user})


@login_required
def summary_reports(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_summary_report.html', {'current_user': current_user})


@login_required
def M2M(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_m2m.html', {'current_user': current_user})


@login_required
def user(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_user.html', {'current_user': current_user})
