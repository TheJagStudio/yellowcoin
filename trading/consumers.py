from .views import dataB
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django_celery_beat.models import PeriodicTask,IntervalSchedule
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async



stocksA = ["INTC:NASDAQ", "AAPL:NASDAQ", "MSFT:NASDAQ", "GOOG:NASDAQ", "AMZN:NASDAQ", "ITC:NSE", "IDEA:NSE",
           "YESBANK:NSE", "BHEL:NSE", "RELIANCE:NSE", "TCS:NSE", "HDFC:NSE", "ICICIBANK:NSE", "MARUTI:NSE", "WIPRO:NSE"]
stocks = ["ITC:NSE", "AAPL:NASDAQ", "RELIANCE:NSE", "TCS:NSE", "HDFC:NSE", "MRF:NSE"]
stocksf = ["ITC:NSE"]

class StockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, Stocks):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in Stocks:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval=schedule, name='every-10-seconds',task="yellowcoin.tasks.update_data", args=json.dumps([Stocks]))


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Parse query_string
        query_params = parse_qs(self.scope["query_string"].decode())
        global stocksf
        for stock in query_params['stock']:
            try:
                index = stocksf.index(stock)
            except:
                index = -1
            if index == -1:
                stocksf.append(stock)
        print(stocksf)
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'message': 'connected'}))


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #print(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_update',
                'message': message
            }
        )
        #print(stocksf)
        global stocksf
        temp = dataB(stocksf)
        await self.send(text_data=json.dumps({'type': 'connect', 'message': temp}))


    async def send_update(self, text):
        self.send(text_data=json.dumps({'type': 'connect', 'message': text}))


'''
class StockConsumer(WebsocketConsumer):
    def addToCeleryBeat(self, stocks):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in stocks:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval=schedule, name='every-10-seconds',task="yellowcoin.tasks.update_data", args=json.dumps([stocks]))

    def connect(self):
        self.room_name = 'trade'
        self.room_group_name = 'stock_%s' % self.room_name

        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        global stocks
        # Parse query string argument
        query_string = parse_qs(self.scope['query_string'].decode())
        stocksf = query_string['stock']
        print(stocksf)
        t = threading.Thread(target=self.addToCeleryBeat, args=(stocksf,))
        t.start()
        #t.join()
        self.accept()
        self.send(text_data=json.dumps({'type' : 'connect', 'message':'connected'}))


    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.close()


    # Receive message from room group
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        print(message)
        channel_layer = get_channel_layer()
        self.channel_layer.send(
            self.channel_name,
            {
                'type': 'send_update',
                'message': message,
            }
        )
        self.send(text_data=json.dumps({'type': 'connect', 'message': message}))

    def send_stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {
                'type': 'stock_update',
                'message': message
            }
        ))

    def send_update(self, text):
        self.send(text_data=json.dumps({'type': 'connect', 'message': text}))

'''