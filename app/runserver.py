from asyncio import gather, get_running_loop
from app.requests_handler import RequestHandler
from logging import getLogger

log = getLogger(__name__)


async def runserver(scope, receive, send):
    try:
        handler = RequestHandler.get_handler(scope)(send)
        await gather(
            handler.consumer(receive),
            loop=get_running_loop()
        )
    except Exception as e:
        log.error(e)
