from uuid import uuid4
from asyncio import sleep, get_running_loop
from json import dumps, loads
from app.cache import CacheGateway


class Handler(object):
    uuid = None
    cache = None
    send = None
    task_end = False
    rooms = []
    user = None
    obj_user = None

    def __init__(self, send):
        self.send = send
        self.uuid = str(uuid4())
        
    async def say_hello(self):
        await self.send({'type': 'websocket.send', 'text': 'hola mundo'})

    async def consumer(self, receive):
        await self.send({'type': 'websocket.accept'})
        self.cache = CacheGateway()
        await self.cache.get_pool()
        await self.say_hello()
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
            # self.cache.lset(self.uuid, message)
            await self.send({'type': 'websocket.send', 'text': message})
            try:
                md = loads(message)
            except:
                return
            if 'action' in md and hasattr(self, md['action']):
                action = getattr(self, md['action'])
                await action(**md['params'])

    async def produce_message(self, text):
        raise NotImplementedError('produce_message not implemented!')
