from app.handlers.handler import Handler
from json import dumps, loads
from uuid import uuid4
from asyncio import sleep, get_running_loop
from app.settings import VELOCITY_PRE_GAME, MAX_ROUND_PER_GAME
from app.resources import movies   


class Judge(Handler):
    connected_users = 0
    codes = set()
    users = dict()
    opcion_correcta = None
    rounds = 0 

    async def say_hello(self):
        await self.get_codes()

    async def produce_message(self, text):
        actions_function = {
            'play': self.play,
            'joined_room': self.joined_room,
            # 'left_room': self.left_room,
        }
        body = loads(text)
        action = body.get('action', None)
        if action in actions_function:
            await actions_function[action](**body.get('params'))

    async def get_codes(self, **kwargs):
        self.codes = ['1234', '4321']
        to_send = dumps(dict(action='get_codes', params=dict(codes=self.codes)))
        await self.send(dict(type='websocket.send', text=to_send))
        self.connected_users = 0
        self.rounds = 1
        self.users = dict()
        for code in self.codes:
            self.cache.set(code, self.uuid)
        subscription, = await self.cache.subscribe(self.uuid)
        get_running_loop().create_task(self.reader(subscription))

    async def _start_play(self, **kwargs):
        for i in range(3, 0, -1):
            to_send = dict(action='starting_play', params=dict(
                time=i, round=self.rounds, users={})
            )
            self.cache.publish_message(self.uuid, to_send)
            await sleep(VELOCITY_PRE_GAME)

        to_send = dict(
                    action='start_play', 
                    params=dict(
                        round=self.rounds,
                        options=[
                            {'key': '1', 'data': movies.movie_1},
                            {'key': '2', 'data': movies.movie_2}
                        ],
                        users={},
                    )
            )
        self.cache.publish_message(self.uuid, to_send)
        self.opcion_correcta = '1'

    async def joined_room(self, user, user_key, **kwargs):
        self.users[user] = {'wons': 0}
        self.codes.remove(user_key)
        if len(self.codes) == 0:
            self.persons = list()
            for key, value in self.users.items():
                person = loads(self.cache.get(key))
                person.update({'wons': 0})
                self.persons.append(person)
            await self._start_play()
        # todo we continue waiting for others users!

    async def play(self, user, answer, **kwargs):
        winner = None
        if answer == self.opcion_correcta:
            winner = user
            index = list(self.users.keys()).index(user)
            self.persons[index]['wons'] += 1

        if self.rounds == MAX_ROUND_PER_GAME:
            to_send = dict(action='end_game', params=dict(users=self.persons))
            self.cache.publish_message(self.uuid, to_send)
            return 
        self.rounds += 1

        to_send = dict(action='end_round', params=dict(won=winner, users=self.persons))
        self.cache.publish_message(self.uuid, to_send)
        await self._start_play()
