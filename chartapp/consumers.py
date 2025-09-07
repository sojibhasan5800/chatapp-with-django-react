from asgiref.sync import sync_to_async
import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        await self.accept()

    async def disconnect(self, close_code):
    
        pass

    async def receive(self, text_data):
     
        pass
