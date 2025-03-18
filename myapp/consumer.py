# my_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WorkerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.worker_id = self.scope['url_route']['kwargs']['worker_id']
        self.room_name = f'worker_{self.worker_id}'  # This defines a unique channel name for each worker
        self.room_group_name = f'worker_{self.worker_id}'

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive notification from the WebSocket group (to send notifications to the worker)
    async def send_notification(self, event):
        notification = event['notification']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification
        }))
