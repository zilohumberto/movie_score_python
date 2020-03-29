import os


REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
API_MOVIE_KEY = os.getenv('API_MOVIE_KEY')
