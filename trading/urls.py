from django.urls import path

from . import views

app_name = 'trading'
urlpatterns = [
    path('', views.home, name='home'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('trades/', views.tradesFunction, name='tradesFunction'),
    path('tradesRemove/', views.tradesRemove, name='tradesRemove'),
    path('data/', views.dataDisplay, name='dataDisplay'),
    path('websocket/', views.ws, name='ws'),
    path('create_transcations/', views.Createtrades, name='Createtrades'),
    path('portfolio/', views.trading_portfolio, name='trading_portfolio'),
    path('ban/', views.trading_ban, name='trading_ban'),
    path('margin/', views.trading_margin, name='trading_margin'),
]
