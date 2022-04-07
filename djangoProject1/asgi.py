import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import chat.routing
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        print(1)
        print(token)
        return token.user
    except Token.DoesNotExist:
        print(2)
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token = next(x for x in scope['headers'] if x[0].decode('utf-8') == 'token')[1].decode('utf-8')
            print(token)
        except Exception:
            token = None
        scope['user'] = AnonymousUser() if token is None else await get_user(token)
        print(scope['user'])
        return await super().__call__(scope, receive, send)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                chat.routing.websocket_urlpatterns
            ))
    ),
})
