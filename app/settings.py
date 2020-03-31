import os


REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6380'))
API_MOVIE_KEY = os.getenv('API_MOVIE_KEY')
VELOCITY_PRE_GAME = float(os.getenv('VELOCITY_PRE_GAME', '1'))