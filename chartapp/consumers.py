from asgiref.sync import sync_to_async
import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode('utf-8')
        params = parse_qs(query_string)
        token =  params.get('token', [None])[0] # token retrieved

        if token:
            try:
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                self.user = await self.get_user(decoded_data['user_id']) #get the user from the token
                self.scope['user'] = self.user

            except jwt.ExpiredSignatureError:
                await self.close(code=4000)
                return
            except jwt.InvalidTokenError:
                await self.close(code=4001)
                return
        else:
            await self.close(code=4002)
            return
        
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
    
        pass

    async def receive(self, text_data):
     
        pass
