from decouple import config

REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = config('REDIS_PORT', default='6380', cast=int)
API_MOVIE_KEY = config('API_MOVIE_KEY', default='')
VELOCITY_PRE_GAME = config('VELOCITY_PRE_GAME', default='1', cast=int)
MAX_ROUND_PER_GAME = config('MAX_ROUND_PER_GAME', default='3', cast=float)
HOST = config('HOST', default='127.0.0.1')
PORT = config('PORT', default='8500', cast=int)
LOG_LEVEL = config('LOG_LEVEL', default='info')
print(HOST, PORT, LOG_LEVEL)