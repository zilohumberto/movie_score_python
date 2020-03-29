import uvicorn
import os  
from app.runserver import runserver

if __name__ == "__main__":
    uvicorn.run(
        runserver,
        ws='auto',
        interface='asgi3',
        loop='asyncio',
        lifespan='off',
        host=os.getenv('HOST','127.0.0.1'),
        port=int(os.getenv('PORT', '8500')),
        log_level=os.getenv('LOG_LEVEL', 'debug'),
        timeout_keep_alive=1000
    )
