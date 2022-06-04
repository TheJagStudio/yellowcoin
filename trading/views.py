from time import time
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
import csv
from kiteconnect import KiteTicker
import random

api = "uha6zxzenz17uw2y"
access = "LpVp9M4hwGjbZVyl44Ako3xyj08ScxJz"
MCX = []
NSE = []
with open("static/all_Symbols.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[11] == "MCX":
            MCX.append(row)
        elif row[11] == "NSE" and row[3] != "":
            NSE.append(row)
count = 0
stockT = []
stocksA = []
for share in NSE:
    if share[3] != "":
        stockT.append(share[3])
        # print(share[3]+" ==> "+share[0]+" : "+share[2])
        count += 1
for share in MCX:
    if share[3] != "":
        stocksA.append(share[2])
        # print(share[3]+" ==> "+share[0]+" : "+share[2])
        count += 1

stocks = ["ITC:NSE", "AAPL:NASDAQ", "RELIANCE:NSE",
          "TCS:NSE", "HDFC:NSE", "MRF:NSE", "YESBANK:NSE"]
dataArrFinal = []
threads = []
counter = 0


"""
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

"""

# new functions


class API:
    def __init__(self, token_to_instrument, api, access):
        self.live_data = {}
        self.token_to_instrument = token_to_instrument
        self.api = api
        self.access = access

    def on_ticks(self, ws, ticks):
        for stock in ticks:
            try:
                self.live_data[self.token_to_instrument[stock['instrument_token']]] = {"Open": stock["ohlc"]["open"],
                                                                                       "High": stock["ohlc"]["high"],
                                                                                       "Low": stock["ohlc"]["low"],
                                                                                       "Close": stock["ohlc"]["close"],
                                                                                       "Last Price": stock["last_price"],
                                                                                       "Volume": stock["volume_traded"],
                                                                                       "change": "%.2f" % stock["change"],
                                                                                       }
            except:
                self.live_data[self.token_to_instrument[stock['instrument_token']]] = {"Open": stock["ohlc"]["open"],
                                                                                       "High": stock["ohlc"]["high"],
                                                                                       "Low": stock["ohlc"]["low"],
                                                                                       "Close": stock["ohlc"]["close"],
                                                                                       "Last Price": stock["last_price"],
                                                                                       "change": "%.2f" % stock["change"],
                                                                                       }

    def on_connect(self, ws, response):
        ws.subscribe(list(self.token_to_instrument.keys()))
        ws.set_mode(ws.MODE_FULL, list(self.token_to_instrument.keys()))

    def Api(self):
        kws = KiteTicker(self.api, self.access)
        kws.on_ticks = self.on_ticks
        kws.on_connect = self.on_connect
        kws.connect(threaded=True)
        while len(self.live_data.keys()) != len(list(self.token_to_instrument.keys())):
            continue

        temp = []
        for i in range(len(list(self.live_data.keys()))):
            temp.append([random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10),
                         random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)])
        x = 0
        for stock in self.live_data.keys():
            try:
                temp[x][0] = stock
                temp[x][1] = self.live_data[stock]["Open"]
                temp[x][2] = self.live_data[stock]["High"]
                temp[x][3] = self.live_data[stock]["Low"]
                temp[x][4] = self.live_data[stock]["Close"]
                temp[x][5] = self.live_data[stock]["Last Price"]
                temp[x][6] = self.live_data[stock]["Volume"]
                temp[x][7] = self.live_data[stock]["change"]
                x += 1
            except:
                temp[x][0] = stock
                temp[x][1] = self.live_data[stock]["Open"]
                temp[x][2] = self.live_data[stock]["High"]
                temp[x][3] = self.live_data[stock]["Low"]
                temp[x][4] = self.live_data[stock]["Close"]
                temp[x][5] = self.live_data[stock]["Last Price"]
                temp[x][6] = "volume"
                temp[x][7] = self.live_data[stock]["change"]
                x += 1
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
    current_user = request.user
    senty = []
    obj = stack.objects.filter(username=request.user).first()
    # obj.stocks = {"data": []}
    # obj.save()
    request.session['live_data'] = {}
    request.session['token_to_instrument_NSE'] = {}
    request.session['token_to_instrument_MCX'] = {}
    request.session['TempNSE'] = {}
    request.session['TempMCX'] = {}
    if obj.stocks['data'] != []:
        for stock in obj.stocks['data']:
            for share in NSE:
                if share[3] == stock:
                    request.session['token_to_instrument_NSE'][int(
                        share[0])] = stock
            for share in MCX:
                if share[2] == stock:
                    request.session['token_to_instrument_MCX'][int(
                        share[0])] = share[2]

        ApiInstance1 = API(
            request.session['token_to_instrument_NSE'], api, access)
        request.session['TempNSE'] = ApiInstance1.Api()
        request.session['TempNSE'].sort(key=lambda x: x[1])
        ApiInstance2 = API(
            request.session['token_to_instrument_MCX'], api, access)
        request.session['TempMCX'] = ApiInstance2.Api()
        request.session['TempMCX'].sort(key=lambda x: x[1])
    ApiInstance2 = API({256265: "NIFTY 50", 265: "SENSEX"}, api, access)
    senty = ApiInstance2.Api()
    if current_user.is_superuser:
        return render(request, 'trade_watchlist.html', {'dataNSE': request.session['TempNSE'], 'dataMCX': request.session['TempMCX'], 'stocksA': stockT, 'stocksB': stocksA, 'current_user': current_user, 'senty': senty, 'market': 'NSE'})
    else:
        return render(request, 'user_trade_watchlist.html', {'dataNSE': request.session['TempNSE'], 'stocksA': stockT, 'dataMCX': request.session['TempMCX'], 'stocksB': stocksA, 'current_user': current_user, 'senty': senty, 'market': 'NSE'})


@login_required
def tradesFunction(request):
    current_user = request.user
    if current_user.is_superuser:
        obj = trades.objects.all()
        return render(request, 'trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksA': stocksA, 'dataArrFinal': dataArrFinal})
    else:
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'user_trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksA': stockT, 'dataArrFinal': dataArrFinal})


@login_required
def Create_market(request):
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
            stopLossPrice = request.POST.get('stopLossPrice')
        if takeProfit != None:
            takeProfitPrice = request.POST.get('takeProfitPrice')
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
    return render(request, 'user_create_market.html', {'trades': obj, 'current_user': current_user, 'stocks': stockT})


@login_required
def Create_limit(request):
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
            stopLossPrice = request.POST.get('stopLossPrice')
        if takeProfit != None:
            takeProfitPrice = request.POST.get('takeProfitPrice')
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
    return render(request, 'user_create_limit.html', {'trades': obj, 'current_user': current_user, 'stocks': stockT})


@login_required
def Create_stop(request):
    current_user = request.user
    obj = trades.objects.filter(user_id=request.user).all()
    return render(request, 'user_create_stop.html', {'trades': obj, 'current_user': current_user, 'stocks': stockT})


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
    stringOutput = {"data": []}
    if apiKey == "asdfghjkl":
        if symbol != None:
            try:
                token_to_instrument_NSE = {}
                for share in NSE:
                    if share[3] == symbol:
                        token_to_instrument_NSE = {int(share[0]): symbol}
                for share in MCX:
                    if share[2] == symbol:
                        token_to_instrument_NSE = {int(share[0]): share[2]}
                ApiInstance3 = API(token_to_instrument_NSE, api, access)
                dataArrFinal = ApiInstance3.Api()
                x = {
                    "name": str(dataArrFinal[0][0]),
                    "open": str(dataArrFinal[0][1]),
                    "high": str(dataArrFinal[0][2]),
                    "low": str(dataArrFinal[0][3]),
                    "close": str(dataArrFinal[0][4]),
                    "last price": str(dataArrFinal[0][5]),
                    "volume": str(dataArrFinal[0][6]),
                    "change": str(dataArrFinal[0][7])
                }
                stringOutput["data"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            userStack = stack.objects.filter(username=request.user.id).first()
            if userStack.stocks['data'] != []:
                token_to_instrument_NSE = {}
                token_to_instrument_MCX = {}
                for stock in userStack.stocks['data']:
                    for share in NSE:
                        if share[3] == stock:
                            token_to_instrument_NSE[int(share[0])] = stock
                    for share in MCX:
                        if share[2] == stock:
                            token_to_instrument_MCX[int(share[0])] = share[2]
                ApiInstance4 = API(token_to_instrument_NSE, api, access)
                dataArrFinal1 = ApiInstance4.Api()
                stringOutput = {"NSE": [], "MCX": []}
                for i in dataArrFinal1:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7])
                    }
                    stringOutput["NSE"].append(x)
                ApiInstance5 = API(token_to_instrument_MCX, api, access)
                dataArrFinal2 = ApiInstance5.Api()
                for i in dataArrFinal2:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7])
                    }
                    stringOutput["MCX"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            else:
                return HttpResponse('No Stocks', content_type="application/json")
    elif apiKey == "qwertyuiop":
        if todo == "get":
            try:
                token_to_instrument_NSE = {}
                for share in NSE:
                    if share[3] == symbol:
                        token_to_instrument_NSE = {int(share[0]): symbol}
                for share in MCX:
                    if share[2] == symbol:
                        token_to_instrument_NSE = {int(share[0]): share[2]}
                ApiInstance3 = API(token_to_instrument_NSE, api, access)
                dataArrFinal = ApiInstance3.Api()
                x = {
                    "name": str(dataArrFinal[0][0]),
                    "open": str(dataArrFinal[0][1]),
                    "high": str(dataArrFinal[0][2]),
                    "low": str(dataArrFinal[0][3]),
                    "close": str(dataArrFinal[0][4]),
                    "last price": str(dataArrFinal[0][5]),
                    "volume": str(dataArrFinal[0][6]),
                    "change": str(dataArrFinal[0][7])
                }
                stringOutput["data"].append(x)
                obj = stack.objects.filter(username=request.user).first()
                obj.stocks['data'].append(symbol)
                obj.save()
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                return HttpResponse(json.dumps({"error": "Invalid Synbol"}), content_type="application/json")
        else:
            print(symbol)
            userStack = stack.objects.filter(username=request.user.id).first()
            userStack.stocks["data"].remove(symbol)
            userStack.save()
            return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponse(HttpResponse('Invalid API Key', content_type="application/json"))
