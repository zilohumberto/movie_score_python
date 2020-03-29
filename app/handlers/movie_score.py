from app.handlers.handler import Handler
from uuid import uuid4
from asyncio import sleep, get_running_loop
from json import dumps, loads


class MovieScore(Handler):
    async def produce_message(self, text):
        actions_function = {
            'join_room': self.join_room,
            'left_room': self.left_room,
            'get_rooms': self.get_rooms,
            'create_room': self.create_room,
            'play': self.play,
        }
        body = loads(text)
        action = body.get('action', None)
        if action in actions_function:
            await actions_function[action](**body.get('params'))

    async def join_room(self, room, **kwargs):
        if room not in self.rooms:
            await self.send(dict(type='websocket.send', text='room dont exist, use create_room'))
            return
        subscription, = await self.cache.subscribe(room)
        get_running_loop().create_task(self.reader(subscription))
        self.user = self.uuid 
        self.cache.publish_message(room, dict(action='joined_room', params=dict(room=room, user=self.user)))

    async def left_room(self, room, **kwargs):
        self.cache.publish_message(room, dict(action='left_room', params=dict(room=room, user=self.user)))

    async def get_rooms(self, **kwargs):
        rooms = self.cache.lget('rooms')
        await self.send(
            {
                'type': 'websocket.send', 
                'text': dumps(
                            {'action': 'get_rooms',
                            'params': {'rooms': rooms}
                            })
            }
        )

    async def create_room(self, room, **kwargs):
        if room in self.rooms:
            await self.send(dict(type='websocket.send', text=f'{room} already exist'))
            return
        self.cache.lset('rooms', room)
        self.rooms.append(room)
        await self.send(dict(type='websocket.send', text=f'room {room} created'))
        await self.join_room(room)
        

    async def play(self, **kwargs):
        pass
    