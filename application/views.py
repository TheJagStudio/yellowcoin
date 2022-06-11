from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
# import csrf
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_user(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        stringOutput = {'status': 'success', 'message': 'Login successful'}
        return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"success": "True"}, indent=4), content_type="application/json")


@csrf_exempt
def get_user(request):
    if request.user.is_authenticated:
        return HttpResponse(json.dumps({"name": request.user.username}, indent=4), content_type="application/json")
