from urllib import parse
from app.handlers.judge import Judge
from app.handlers.movie_score import MovieScore


class RequestHandler:
    """
        Translation necessary between requests and server
        Able to translate header and url into json
    """

    @classmethod
    def get_handler(cls, scope):
        client = cls.get_client(scope)
        if client=='judge':
            return Judge
        if client =='movie':
            return MovieScore
        return None

    @classmethod
    def get_client(cls, scope):
        query_dict = cls._parse_query_string(scope.get('query_string', b"")) 
        return query_dict.get('client', 'judge').lower()

    @staticmethod
    def _parse_query_string(query_string):
        """
        Converts the given query_string into a dictionary. Returns an empty dict if the operation fails.
        :param query_string:
        :return: query string as dict.
        """
        try:
            query_string = query_string.decode('utf-8')
            return dict(parse.parse_qsl(query_string))
        except (UnicodeDecodeError, AttributeError):
            return dict()
