from asyncio import gather, get_running_loop
from app.handlers.movie_score import MovieScore
from logging import getLogger

log = getLogger(__name__)


async def runserver(scope, receive, send):
    try:
        handler = MovieScore(send)
        await send({'type': 'websocket.accept'})
        await send({'type': 'websocket.send', 'text': 'hola mundo'})
        await gather(
            handler.consumer(receive),
            loop=get_running_loop()
        )
    except Exception as e:
        log.error(e)
