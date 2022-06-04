from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def forex_wacthlist(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_watchlist.html', {'current_user': current_user})
    else:
        return render(request, 'user_forex_watchlist.html', {'current_user': current_user})


@login_required
def forex_trades(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_trades.html', {'current_user': current_user})
    else:
        return render(request, 'user_forex_trades.html', {'current_user': current_user})


@login_required
def forex_portfolio(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_portfolio.html', {'current_user': current_user})
    else:
        return render(request, 'user_forex_portfolio.html', {'current_user': current_user})


@login_required
def forex_margin(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_margin.html', {'current_user': current_user})
