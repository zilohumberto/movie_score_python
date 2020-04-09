import uvicorn
from app.settings import HOST, PORT, LOG_LEVEL
from app.runserver import runserver

if __name__ == "__main__":
    uvicorn.run(
        runserver,
        ws='auto',
        interface='asgi3',
        loop='asyncio',
        lifespan='off',
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        timeout_keep_alive=1000
    )
