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
        #remove group from channel:
        await self.channel_layer.group_discard(
            self.channel_layer,
            self.room_group_name
        )

    #handles what happens when we receive a particular message:
    async def receive(self, message_data):
        data = json.loads(message_data) #loads the data as json
        #decode the data it received:
        message = data['message']
        username = data['username']
        room = data['room']

        #create function to send data to the channel_layer group:
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type':'chat_message',
                'message':message,
                'username': username, 
                'room': room
            }
        )

    #send message to the room:
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data = json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

#consumer has been configured to receive a message and send it back to the client
#we need to receive the message inside the client and display it