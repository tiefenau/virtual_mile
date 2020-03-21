# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Trinker, Bier, Pruegel, Busfahrt, Bussitzer
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "trinker_room",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        #message = text_data_json['message']

        if(type == "hauen"):
            hit = text_data_json['opfer']
            hitter = text_data_json['hauer']
            hauer = User.objects.get(username=hitter)
            geschlagen = User.objects.get(username=hit)
            Pruegel.objects.create(schlaeger=hauer.trinker, geschlagen=geschlagen.trinker)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'hauen',
                    'hit': hit,
                    'hitter': hitter,
                    'newcount': geschlagen.trinker.geschlagen.count()
                }
            )
        elif (type=="trink"):
            trinkername = text_data_json['trinker']
            t = User.objects.get(username=trinkername)
            Bier.objects.create(trinker=t.trinker)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'trinken',
                    'trinker': trinkername,
                    'newcount': t.trinker.biere.count()
                }
            )
        elif (type=="busstart"):
            fahrt = Busfahrt.objects.create()
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'busstart',
                    'fahrt_id': fahrt.id
                }
            )
        elif (type=="einsteigen"):
            fahrt_id = text_data_json['fahrt_id']
            trinkername = text_data_json['fahrer']
            t = User.objects.get(username=trinkername)
            fahrt = Busfahrt.objects.get(id=fahrt_id)
            Bussitzer.objects.create(fahrt = fahrt, fahrer = t.trinker)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'einstieg',
                    'trinker': trinkername
                }
            )
        elif (type=="losfahren"):
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'losfahren',
                }
            )
        #self.send(text_data=json.dumps({
        #    'message': 'test'+message
        #}))
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))

    def trinken(self, event):
        trinker = event['trinker']
        newcount = event['newcount']
        self.send(text_data=json.dumps({
            'type': 'trink',
            'trinker': trinker,
            'newcount': newcount
        }))

    def hauen(self, event):
        hit = event['hit']
        hitter = event['hitter']
        newcount = event['newcount']
        self.send(text_data=json.dumps({
            'type': 'hauen',
            'hit': hit,
            'hitter': hitter,
            'newcount': newcount
        }))

    def busstart(self, event):
        self.send(text_data=json.dumps({
            'type': 'busstart',
            'fahrt_id': event['fahrt_id']
        }))

    def einstieg(self, event):
        trinker = event['trinker']
        self.send(text_data=json.dumps({
            'type': 'einstieg',
            'trinker': trinker,
        }))

    def losfahren(self, event):
        self.send(text_data=json.dumps({
            'type': 'losfahren',
        }))
