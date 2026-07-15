import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "chat_room"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message_type = data["type"]

        if message_type == "message":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": data["message"],
                    "username": data["username"]
                }
            )

        elif message_type == "typing":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "typing_indicator",
                    "username": data["username"],
                }
            )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": event["message"],
                    "username": event["username"]
                }
            )
        )

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"]
        }))