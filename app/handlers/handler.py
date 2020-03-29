from uuid import uuid4
from asyncio import sleep, get_running_loop
from json import dumps, loads
from app.cache import CacheGateway


class Handler(object):
    uuid = str(uuid4())
    cache = None
    send = None
    task_end = False
    rooms = []
    user = None
    obj_user = None

    def __init__(self, send):
        self.send = send

    async def consumer(self, receive):
        self.cache = CacheGateway()
        await self.cache.get_pool()
        self.rooms = self.cache.lget('rooms')
        while True:
            try:
                message = await receive()
            except Exception as e:
                raise Exception("consumer error")
            
            if self.task_end:
                break

            if message.get('type') == 'websocket.disconnect':
                for room in self.rooms:
                    await self.left_room(room)
                self.task_end = True
                raise Exception("task end")

            if message.get('type') == 'websocket.connect':
                continue
            text = message['text']
            await self.produce_message(text)
            await sleep(0.1)

    async def reader(self, channel):
        async for message in channel.iter():
            try:
                message = message.decode('utf-8')
            except:
                self.task_end = True
                raise Exception()
            self.cache.lset(self.uuid, message)
            await self.send({'type': 'websocket.send', 'text': message})

    async def produce_message(self, text):
        raise NotImplementedError('produce_message not implemented!')