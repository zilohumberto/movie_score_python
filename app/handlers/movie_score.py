from app.handlers.handler import Handler
from uuid import uuid4
from asyncio import sleep, get_running_loop
from json import dumps, loads


class MovieScore(Handler):
    room = None

    async def produce_message(self, text):
        actions_function = {
            'join_room': self.join_room,
            'left_room': self.left_room,
            'play': self.play,
        }
        body = loads(text)
        action = body.get('action', None)
        if action in actions_function:
            await actions_function[action](**body.get('params'))

    async def join_room(self, user_key, **kwargs):
        code = self.cache.get(user_key)
        if not code:
            to_send = dumps(dict(action='invalid_code', params={}))
            await self.send(dict(type='websocket.send', text=to_send))
            return
        to_send = dumps(dict(action='accepted_code', params={}))
        await self.send(dict(type='websocket.send', text=to_send))
        self.cache.delete(user_key)
        self.room = code
        self.cache.publish_message(
            self.room, 
            dict(action='joined_room', params=dict(user=self.uuid, user_key=user_key))
        ) 
        
    async def left_room(self, **kwargs):
        self.cache.publish_message(self.room, dict(action='left_room', params=dict(user=self.uuid)))
        self.room = None

    async def play(self, **kwargs):
        self.cache.publish_message(self.room, dict(action='play', params=dict(user=self.uuid, **kwargs))) 
