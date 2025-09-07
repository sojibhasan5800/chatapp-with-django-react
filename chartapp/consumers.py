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

        user_data = await self.get_user_data(self.user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'online_users': [user_data],
                'status': 'online',
            }
        )



    async def disconnect(self, close_code):
        
        if hasattr(self, 'room_group_name'):

            user_data = await self.get_user_data(self.scope["user"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'online_users': [user_data],
                    'status': 'offline',
                }
            )

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            

    async def receive(self, text_data):
     
        pass
