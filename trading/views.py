from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium import webdriver
from kiteconnect import KiteConnect
from time import sleep
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import stack
from .models import trades
import requests
from bs4 import BeautifulSoup
import json
import threading
import csv
from kiteconnect import KiteTicker
from alpaca_trade_api.rest import REST, TimeFrame
import random
from user.models import UserAccount
import os
from django.views.decorators.csrf import csrf_exempt
import threading


api = "uha6zxzenz17uw2y"
secret = "cwdawxqyp6c0dgdljvffpi4k4nhejnbm"
f = open("static/config.txt", "r")
access = str(f.read())
print(access)
MCX = []
NSE = []
NFO = []
headers = {
    'X-Kite-Version': '3',
    'Authorization': 'token '+api+':'+access,
}
with open("static/all_Symbols.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[11] == "MCX":
            MCX.append(row)
        elif row[11] == "NSE" and row[3] != "":
            NSE.append(row)
        elif row[11] == "NFO" and row[3] != "":
            NFO.append(row)
count = 0
stockT = []
stocksA = []
stocksB = []
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
for share in NFO:
    if share[3] != "":
        stocksB.append(share[2])
        # print(share[3]+" ==> "+share[0]+" : "+share[2])
        count += 1
print(len(stocksA))
print(len(stocksB))
print(len(stockT))

stocks = ["ITC:NSE", "AAPL:NASDAQ", "RELIANCE:NSE",
          "TCS:NSE", "HDFC:NSE", "MRF:NSE", "YESBANK:NSE"]
dataArrFinal = []
threads = []
counter = 0


def access_gen(request):
    global api, secret
    f = open("static/config.txt", "r")
    access = str(f.read())
    print(access)
    kite = KiteConnect(api_key=api)
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    except:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(
            executable_path=chromedriver_autoinstaller.install(), chrome_options=chrome_options)
    driver.get(kite.login_url())
    sleep(2)
    password = driver.find_element(By.ID, "userid")
    password.click()
    password.send_keys("YQ0474")
    password = driver.find_element(By.ID, "password")
    password.click()
    password.send_keys("Vishal@123")
    submitBtn = driver.find_element(By.TAG_NAME, "button")
    submitBtn.click()
    sleep(1)
    password = driver.find_element(By.ID, "pin")
    password.click()
    password.send_keys("300689")
    submitBtn = driver.find_element(By.TAG_NAME, "button")
    submitBtn.click()
    sleep(1)
    newurl = driver.current_url
    driver.close()
    request_token = newurl.split("request_token=")[1].split("&")[0]
    gen_ssn = kite.generate_session(
        request_token=request_token, api_secret=secret)
    access = gen_ssn['access_token']
    print(access)
    f = open("static/config.txt", "w")
    f.write(access)
    f.close()
    kite.set_access_token(access_token=access)
    return HttpResponse(access)


def access_gen_to_use():
    global api, secret
    f = open("static/config.txt", "r")
    access = str(f.read())
    print(access)
    kite = KiteConnect(api_key=api)
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    except:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(
            executable_path=chromedriver_autoinstaller.install(), chrome_options=chrome_options)
    driver.get(kite.login_url())
    sleep(2)
    password = driver.find_element(By.ID, "userid")
    password.click()
    password.send_keys("YQ0474")
    password = driver.find_element(By.ID, "password")
    password.click()
    password.send_keys("Vishal@123")
    submitBtn = driver.find_element(By.TAG_NAME, "button")
    submitBtn.click()
    sleep(1)
    password = driver.find_element(By.ID, "pin")
    password.click()
    password.send_keys("300689")
    submitBtn = driver.find_element(By.TAG_NAME, "button")
    submitBtn.click()
    sleep(1)
    newurl = driver.current_url
    driver.close()
    request_token = newurl.split("request_token=")[1].split("&")[0]
    gen_ssn = kite.generate_session(
        request_token=request_token, api_secret=secret)
    access = gen_ssn['access_token']
    print(access)
    f = open("static/config.txt", "w")
    f.write(access)
    f.close()
    kite.set_access_token(access_token=access)


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


def ApiF(market, token):
    global api
    f = open("static/config.txt", "r")
    access = str(f.read())
    headers = {
        'X-Kite-Version': '3',
        'Authorization': 'token '+api+':'+access,
    }
    stocks = ""
    for stock in token:
        stocks += "i="+market+":"+stock+"&"
    # remove last character
    stocks = stocks[:-1]
    response = requests.get(
        'https://api.kite.trade/quote?'+stocks, headers=headers)
    live_data = response.json()['data']
    temp = []
    name = ""
    for i in range(len(token)):
        if market == "NSE":
            for share in NSE:
                if share[2] == token[i]:
                    name = share[3]
        else:
            name = token[i]
        symbols = market+":"+token[i]
        try:
            temp.append([name, live_data[symbols]["ohlc"]["open"], live_data[symbols]["ohlc"]["high"], live_data[symbols]["ohlc"]["low"], live_data[symbols]["ohlc"]["close"],
                         live_data[symbols]["last_price"], live_data[symbols]["volume"], live_data[symbols]["net_change"], live_data[symbols]["depth"]["buy"][0]["price"], live_data[symbols]["depth"]["sell"][0]["price"]])
        except:
            temp.append([name, live_data[symbols]["ohlc"]["open"], live_data[symbols]["ohlc"]["high"], live_data[symbols]["ohlc"]["low"], live_data[symbols]["ohlc"]["close"],
                         live_data[symbols]["last_price"], "volume", live_data[symbols]["net_change"], "0", "0"])
    return temp


@ login_required
def home(request):
    """current_user = request.user
    if current_user.username == 'admin':
        return render(request, 'home.html', {'current_user': current_user})
    else:
        return render(request, 'user_home.html', {'current_user': current_user})"""
    return redirect('trading:watchlist')


@ login_required
def ws(request):
    obj = stack.objects.filter(username=request.user).first()
    context = {'stocks': obj.stocks['data']}

    return render(request, 'websockets.html', context=context)


@ login_required
def watchlist(request):
    f = open("static/config.txt", "r")
    access = str(f.read())
    try:
        current_user = request.user
        senty = []
        obj = stack.objects.filter(username=request.user).first()
        # obj.stocks = {"data": []}
        # obj.save()
        request.session['live_data'] = {}
        request.session['token_to_instrument_NSE'] = []
        request.session['token_to_instrument_MCX'] = []
        request.session['token_to_instrument_NFO'] = []
        request.session['TempNSE'] = []
        request.session['TempMCX'] = []
        request.session['TempNFO'] = []
        if obj.stocks['data'] != []:
            for stock in obj.stocks['data']:
                for share in NSE:
                    if share[3] == stock:
                        request.session['token_to_instrument_NSE'].append(
                            share[2])
                for share in MCX:
                    if share[2] == stock:
                        request.session['token_to_instrument_MCX'].append(
                            share[2])
                for share in NFO:
                    if share[2] == stock:
                        request.session['token_to_instrument_NFO'].append(
                            share[2])

            request.session['TempNSE'] = ApiF(
                "NSE", request.session['token_to_instrument_NSE'])
            request.session['TempMCX'] = ApiF(
                "MCX", request.session['token_to_instrument_MCX'])
            request.session['TempNFO'] = ApiF(
                "NFO", request.session['token_to_instrument_NFO'])
            request.session['TempNSE'].sort(key=lambda x: x[1])
            request.session['TempMCX'].sort(key=lambda x: x[1])
            request.session['TempNFO'].sort(key=lambda x: x[1])
        senty = [ApiF("NSE", ["NIFTY 50"]), ApiF("BSE", ["SENSEX"])]
        if current_user.is_superuser:
            return render(request, 'trade_watchlist.html', {'dataNSE': request.session['TempNSE'], 'dataMCX': request.session['TempMCX'], 'dataNFO': request.session['TempNFO'], 'stocksA': stockT, 'stocksB': stocksA, 'stocksC': stocksB, 'current_user': current_user, 'senty': senty, 'market': 'NSE'})
        else:
            user_account = UserAccount.objects.filter(
                user=current_user).first()
            if user_account.Account_Type == "User":
                givenUser = "False"
            else:
                givenUser = "True"
            return render(request, 'user_trade_watchlist.html', {'dataNSE': request.session['TempNSE'], 'dataNFO': request.session['TempNFO'], 'dataMCX': request.session['TempMCX'], 'givenUser': givenUser, 'stocksA': stockT, 'stocksB': stocksA, 'stocksC': stocksB, 'current_user': current_user, 'senty': senty, 'market': 'NSE'})
    except:
        access_gen_to_use()
        return redirect('trading:watchlist')


@ login_required
def tradesFunction(request):
    current_user = request.user
    if current_user.is_superuser:
        obj = trades.objects.all()
        return render(request, 'trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksA': stocksA, 'dataArrFinal': dataArrFinal})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'user_trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksA': stockT, 'dataArrFinal': dataArrFinal, 'givenUser': givenUser})


@ login_required
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


@ login_required
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


@ login_required
def Create_stop(request):
    current_user = request.user
    obj = trades.objects.filter(user_id=request.user).all()
    return render(request, 'user_create_stop.html', {'trades': obj, 'current_user': current_user, 'stocks': stockT})


@ login_required
def trading_portfolio(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_portfolio.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_trading_portfolio.html', {'current_user': current_user, 'givenUser': givenUser})


@ login_required
def trading_ban(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_ban.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_trading_ban.html', {'current_user': current_user, 'givenUser': givenUser})


@ login_required
def trading_margin(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_margin.html', {'current_user': current_user})


@ login_required
def tradesRemove(request):
    id = request.GET.get('id')
    trades.objects.filter(id=id).delete()
    return HttpResponse("success")


@ csrf_exempt
@ login_required
def dataDisplay(request):
    # args = request.args
    apiKey = request.GET.get('apiKey')
    symbol = request.GET.get('symbol')
    market = request.GET.get('segment')
    todo = request.GET.get('todo')
    print(apiKey, symbol)
    stringOutput = {"data": []}
    if apiKey == "asdfghjkl":
        if symbol != None:
            try:
                token_to_instrument_NSE = []
                for share in NSE:
                    if share[3] == symbol:
                        token_to_instrument_NSE.append(share[2])
                for share in MCX:
                    if share[2] == symbol:
                        token_to_instrument_NSE.append(share[2])
                for share in NFO:
                    if share[2] == symbol:
                        token_to_instrument_NSE.append(share[2])
                dataArrFinal = ApiF("NSE", [stock])
                x = {
                    "name": str(dataArrFinal[0][0]),
                    "open": str(dataArrFinal[0][1]),
                    "high": str(dataArrFinal[0][2]),
                    "low": str(dataArrFinal[0][3]),
                    "close": str(dataArrFinal[0][4]),
                    "last price": str(dataArrFinal[0][5]),
                    "volume": str(dataArrFinal[0][6]),
                    "change": str(dataArrFinal[0][7]),
                    "bid": str(dataArrFinal[0][8]),
                    "ask": str(dataArrFinal[0][9]),
                }
                stringOutput["data"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            userStack = stack.objects.filter(username=request.user.id).first()
            if userStack.stocks['data'] != []:
                token_to_instrument_NSE = []
                token_to_instrument_MCX = []
                token_to_instrument_NFO = []
                for stock in userStack.stocks['data']:
                    for share in NSE:
                        if share[3] == stock:
                            token_to_instrument_NSE.append(share[2])
                    for share in MCX:
                        if share[2] == stock:
                            token_to_instrument_MCX.append(share[2])
                    for share in NFO:
                        if share[2] == stock:
                            token_to_instrument_NFO.append(share[2])
                dataArrFinal1 = []
                dataArrFinal1 = ApiF("NSE", token_to_instrument_NSE)
                stringOutput = {"NSE": [], "MCX": [], "NFO": []}
                for i in dataArrFinal1:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["NSE"].append(x)
                dataArrFinal2 = []
                dataArrFinal = ApiF("MCX", token_to_instrument_MCX)
                for i in dataArrFinal2:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["MCX"].append(x)
                dataArrFinal3 = []
                dataArrFinal = ApiF("NFO", token_to_instrument_NFO)
                for i in dataArrFinal3:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["NFO"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            else:
                return HttpResponse('No Stocks', content_type="application/json")
    elif apiKey == "qwertyuiop":
        if todo == "get":
            try:
                stock = []
                if market == "NSE":
                    for share in NSE:
                        if share[3] == symbol:
                            stock.append(share[2])
                    dataArrFinal = ApiF("NSE", stock)
                elif market == "MCX":
                    for share in MCX:
                        if share[2] == symbol:
                            stock.append(share[2])
                    dataArrFinal = ApiF("MCX", stock)
                elif market == "NFO":
                    for share in NFO:
                        if share[2] == symbol:
                            stock.append(share[2])
                    dataArrFinal = ApiF("NFO", stock)
                x = {
                    "name": str(dataArrFinal[0][0]),
                    "open": str(dataArrFinal[0][1]),
                    "high": str(dataArrFinal[0][2]),
                    "low": str(dataArrFinal[0][3]),
                    "close": str(dataArrFinal[0][4]),
                    "last price": str(dataArrFinal[0][5]),
                    "volume": str(dataArrFinal[0][6]),
                    "change": str(dataArrFinal[0][7]),
                    "bid": str(dataArrFinal[0][8]),
                    "ask": str(dataArrFinal[0][9]),
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
            return HttpResponse(json.dumps({"success": "True"}), content_type="application/json")
    else:
        return HttpResponse(HttpResponse('Invalid API Key', content_type="application/json"))
