from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        #function responsible for getting room name or chat group name
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #gives us name of room
        self.room_group_name='chat_%s' % self.room_name #gives us group name

        #code to connect to particular room: take particular channel and add specific room (above) to that channel
        #takes channel layer and adds the room group name to it
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        ) #this is a function call, because it is aync, I need to add await to the f(x) call

        await self.accept() #accepts incoming connection


    #function to handle disconnecting:
    async def disconnect(self):
        #remove group fomr channel:
        await self.channel_layer.group_discard(
            self.channel_layer,
            self.room_group_name
        )
