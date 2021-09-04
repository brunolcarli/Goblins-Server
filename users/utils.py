'''
Módule for user tools definition.
'''
from datetime import datetime, date
from functools import wraps
from users.models import TokenBlackList


# A principio so funciona se o token vier na forma:
# "Authorization": "JWT token""
# TODO implementar uma alterantiva para receber Bearer token
def access_required(function):
    """
    Verify if the user is logged on the system.
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        user_token = args[1].context.META.get('HTTP_AUTHORIZATION')
        is_black_listed = TokenBlackList.objects.filter(token=user_token)
        if is_black_listed:
            raise Exception('Session Expired, please log in again!')

        user = args[1].context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return function(*args, **kwargs)
    return decorated
