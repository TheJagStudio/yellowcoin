from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import stack
from .models import trades
import requests
from bs4 import BeautifulSoup
import json
import threading
from django.utils import timezone
from alpaca_trade_api.rest import REST, TimeFrame

stocksA = ["INTC:NASDAQ", "AAPL:NASDAQ", "MSFT:NASDAQ", "GOOG:NASDAQ", "AMZN:NASDAQ", "ITC:NSE", "IDEA:NSE",
           "YESBANK:NSE", "BHEL:NSE", "RELIANCE:NSE", "TCS:NSE", "HDFC:NSE", "ICICIBANK:NSE", "MARUTI:NSE", "WIPRO:NSE"]
stocks = ["ITC:NSE", "AAPL:NASDAQ", "RELIANCE:NSE",
          "TCS:NSE", "HDFC:NSE", "MRF:NSE", "YESBANK:NSE"]
dataArrFinal = []
threads = []
counter = 0
BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_API_KEY = "PKE4DCHDAKBV3I1LVF8U"
ALPACA_SECRET_KEY = "JklTIDiJlyJskZ9jMeUkapLT6xX2aHykX2E5twEO"

api = REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY,
           base_url=BASE_URL, api_version='v2')


def thread_function(i, stocks):
    global dataArrFinal
    dataArr = []
    url = "https://www.google.com/finance/quote/"+stocks[i]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('div', attrs={"class": "YMlKec fxKbKc"})
    data = soup.find_all('div', attrs={"class": "P6K39c"})
    dataArr.append(stocks[i])
    dataArr.append(price.text)
    for j in range(0, 7):
        dataArr.append(data[j].text)
    dataArrFinal.append(dataArr)
    dataArr = []
    # print(stocks[i])


def dataB(stocks):
    global dataArrFinal, threads
    for i in range(0, len(stocks)):
        t = threading.Thread(target=thread_function, args=(i, stocks))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    temp = dataArrFinal
    dataArrFinal = []
    threads = []
    return temp


def data(stock):
    global dataArrFinal
    dataArr = []
    url = "https://www.google.com/finance/quote/"+stock
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('div', attrs={"class": "YMlKec fxKbKc"})
    data = soup.find_all('div', attrs={"class": "P6K39c"})
    dataArr.append(stock)
    dataArr.append(price.text)
    for j in range(0, 7):
        try:
            dataArr.append(data[j].text)
        except:
            pass
    dataArrFinal = dataArr
    dataArr = []
    # print(stock)
    temp = dataArrFinal
    dataArrFinal = []
    return temp


@login_required
def home(request):
    """current_user = request.user
    if current_user.username == 'admin':
        return render(request, 'home.html', {'current_user': current_user})
    else:
        return render(request, 'user_home.html', {'current_user': current_user})"""
    return redirect('trading:watchlist')


@login_required
def ws(request):
    obj = stack.objects.filter(username=request.user).first()
    context = {'stocks': obj.stocks['data']}

    return render(request, 'websockets.html', context=context)


@login_required
def watchlist(request):
    obj = stack.objects.filter(username=request.user).first()
    # obj.stocks = {"data": []}
    # obj.save()
    temp = dataB(obj.stocks["data"])
    temp.sort(key=lambda x: x[1])
    current_user = request.user
    senty = [[], []]
    senty[0] = data("NIFTY_50:INDEXNSE")
    senty[1] = data("SENSEX:INDEXBOM")
    if current_user.is_superuser:
        return render(request, 'trade_watchlist.html', {'dataArrFinal': temp, 'stocksA': stocksA, 'current_user': current_user, 'senty': senty})
    else:
        return render(request, 'user_trade_watchlist.html', {'dataArrFinal': temp, 'stocksA': stocksA, 'current_user': current_user, 'senty': senty})


@login_required
def tradesFunction(request):
    obj = trades.objects.filter(user_id=request.user).all()
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksA': stocksA, 'dataArrFinal': dataArrFinal})
    else:
        return render(request, 'user_trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksA': stocksA, 'dataArrFinal': dataArrFinal})


@login_required
def Createtrades(request):
    current_user = request.user
    if (request.method == 'POST'):
        symbol = request.POST.get('symbol')
        type = request.POST.get('type')
        amount = request.POST.get('amount')
        takeProfit = request.POST.get('takeProfit')
        stopLoss = request.POST.get('stopLoss')
        stopLossPrice = ''
        takeProfitPrice = ''
        if stopLoss != None:
            stopLossPrice = request.POST.get('Loss_Price')
        if takeProfit != None:
            takeProfitPrice = request.POST.get('Profit_Price')
        print(symbol, type, amount, takeProfit,
              stopLoss, stopLossPrice, takeProfitPrice)
        if takeProfitPrice == '' and stopLossPrice == '':
            order = api.submit_order(
                symbol=symbol,
                qty=amount,
                side=type,
                type='market',
                time_in_force='day',
            )
        elif(takeProfitPrice != '' and stopLossPrice != ''):
            order = api.submit_order(
                symbol=symbol,
                qty=amount,
                side=type,
                type='market',
                time_in_force='day',
                take_profit=dict(
                    limit_price=takeProfitPrice,
                ),
                stop_loss=dict(
                    stop_price=stopLossPrice,
                    limit_price=stopLossPrice,
                )
            )
        elif(takeProfitPrice != ''):
            order = api.submit_order(
                symbol=symbol,
                qty=amount,
                side=type,
                type='market',
                time_in_force='day',
                take_profit=dict(
                    limit_price=takeProfitPrice,
                ),
            )
        elif(stopLossPrice != ''):
            order = api.submit_order(
                symbol=symbol,
                qty=amount,
                side=type,
                type='market',
                time_in_force='day',
                stop_loss=dict(
                    stop_price=stopLossPrice,
                    limit_price=stopLossPrice,
                )
            )
        else:
            pass
        print("Order ID:", order.id)
        print("Order Status:", order.status)
        print("Order Qty:", order.qty)
        print("Order Type:", order.type)
        print("Order Symbol:", order.symbol)
        print("buy price:", order.limit_price)
        data = api.get_bars(symbol, TimeFrame.Hour, "2021-05-26",
                            "2022-05-26",  limit=1)
        orderPrice = data[0].o
        print("Order Price:", orderPrice)
        newTrade = trades(user_id=request.user, script=str(symbol),
                          orderType=str(type), qty=int(amount), status=str(order.status), orderPrice=float(orderPrice), market="NASDAQ", bs=str(str(data[0].h)+'/'+str(data[0].l)), lot=int(1))
        newTrade.save()
    obj = trades.objects.filter(user_id=request.user).all()
    stocksT = ['IPVI', 'IPVIU', 'IPW', 'CMBM', 'CMCA', 'PCOM', 'ARTEU',  'WAVD', 'DDI', 'PUI', 'PULM',
               'VCYT', 'DEMZ', 'STNE', 'DENN', 'DERM', 'KLAC', 'KLAQ', 'WAVE',  'PAVM', 'IPSC', 'PAX', 'CGEN']
    return render(request, 'user_create_transcations.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksT})


@login_required
def trading_portfolio(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_portfolio.html', {'current_user': current_user})
    else:
        return render(request, 'user_trading_portfolio.html', {'current_user': current_user})


@login_required
def trading_ban(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_ban.html', {'current_user': current_user})
    else:
        return render(request, 'user_trading_ban.html', {'current_user': current_user})


@login_required
def trading_margin(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_margin.html', {'current_user': current_user})


@login_required
def tradesRemove(request):
    id = request.GET.get('id')
    trades.objects.filter(id=id).delete()
    return HttpResponse("success")


@login_required
def dataDisplay(request):
    # args = request.args
    apiKey = request.GET.get('apiKey')
    symbol = request.GET.get('symbol')
    todo = request.GET.get('todo')
    print(apiKey, symbol)
    if apiKey == "asdfghjkl":
        if symbol != None:
            try:
                dataArrFinal = data(symbol)
                stringOutput = {"data": []}
                x = {
                    "name": str(dataArrFinal[0]),
                    "price": str(dataArrFinal[1]),
                    "priviousClose": str(dataArrFinal[2]),
                    "dayRange": str(dataArrFinal[3]),
                    "yearRange": str(dataArrFinal[4]),
                    "volume": str(dataArrFinal[5]),
                    "peRatio": str(dataArrFinal[6]),
                    "dividentYield": str(dataArrFinal[7]),
                    "stockExchange": str(dataArrFinal[8])
                }
                stringOutput["data"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            userStack = stack.objects.filter(username=request.user.id).first()
            dataArrFinal = dataB(userStack.stocks["data"])
            stringOutput = {"data": []}
            for i in dataArrFinal:
                x = {
                    "name": str(i[0]),
                    "price": str(i[1]),
                    "priviousClose": str(i[2]),
                    "dayRange": str(i[3]),
                    "yearRange": str(i[4]),
                    "volume": str(i[5]),
                    "peRatio": str(i[6]),
                    "dividentYield": str(i[7]),
                    "stockExchange": str(i[8])
                }
                stringOutput["data"].append(x)
            return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
    elif apiKey == "qwertyuiop":
        if todo == "get":
            print("get")
            try:
                dataArrFinal = data(symbol)
                stringOutput = {"data": []}
                x = {
                    "name": str(dataArrFinal[0]),
                    "price": str(dataArrFinal[1]),
                    "priviousClose": str(dataArrFinal[2]),
                    "dayRange": str(dataArrFinal[3]),
                    "yearRange": str(dataArrFinal[4]),
                    "volume": str(dataArrFinal[5]),
                    "peRatio": str(dataArrFinal[6]),
                    "dividentYield": str(dataArrFinal[7]),
                    "stockExchange": str(dataArrFinal[8])
                }
                stringOutput["data"].append(x)
                userStack = stack.objects.filter(
                    username=request.user.id).first()
                userStack.stocks["data"].append(symbol)
                userStack.save()
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                print("error")
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            print(symbol)
            userStack = stack.objects.filter(username=request.user.id).first()
            userStack.stocks["data"].remove(symbol)
            userStack.save()
            return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponse(HttpResponse('Invalid API Key', content_type="application/json"))
