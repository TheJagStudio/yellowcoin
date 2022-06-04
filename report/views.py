from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def track_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_track.html', {'current_user': current_user})


@login_required
def ledge_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_ledge.html', {'current_user': current_user})
    else:
        return render(request, 'user_report_ledge.html', {'current_user': current_user})


@login_required
def deposit_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_deposit.html', {'current_user': current_user})
    else:
        return render(request, 'user_report_deposit.html', {'current_user': current_user})


@login_required
def trail_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_trail.html', {'current_user': current_user})


@login_required
def client_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_client.html', {'current_user': current_user})
