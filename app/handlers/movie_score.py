from app.handlers.handler import Handler
from uuid import uuid4
from asyncio import sleep, get_running_loop
from json import dumps, loads
from requests import get


class MovieScore(Handler):
    room = None

    async def produce_message(self, text):
        actions_function = {
            'join_room': self.join_room,
            'left_room': self.left_room,
            'play': self._play,
        }
        body = loads(text)
        action = body.get('action', None)
        if action in actions_function:
            await actions_function[action](**body.get('params'))

    def get_person(self):
        r = get(url="https://randomuser.me/api/?results=1")
        if r.status_code != 200:
            return
        person = loads(r.text)
        return person['results'][0]

    async def join_room(self, user_key, **kwargs):
        code = self.cache.get(user_key)
        if not code:
            to_send = dumps(dict(action='invalid_code', params={}))
            await self.send(dict(type='websocket.send', text=to_send))
            return

        person = self.get_person()
        to_send = dumps(dict(action='accepted_code', params=dict(person=person)))
        
        await self.send(dict(type='websocket.send', text=to_send))
        self.cache.delete(user_key)
        self.cache.set(self.uuid, person, expires=600)
        self.room = code
        self.cache.publish_message(
            self.room, 
            dict(action='joined_room', params=dict(user=self.uuid, user_key=user_key))
        )
        subscription, = await self.cache.subscribe(self.room)
        get_running_loop().create_task(self.reader(subscription))
        
    async def left_room(self, **kwargs):
        self.cache.publish_message(self.room, dict(action='left_room', params=dict(user=self.uuid)))
        self.room = None

    async def _play(self, **kwargs):
        self.cache.publish_message(self.room, dict(action='play', params=dict(user=self.uuid, **kwargs))) 

    # async def play(self, **kwargs):
    #     # a opponent play before you? yes