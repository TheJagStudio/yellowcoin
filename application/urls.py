from django.urls import path
from . import views

app_name = 'application'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('get_user/', views.get_user, name='get_user'),
]
