import channels
import channels.auth
import django
import django.core.asgi
from game_server.schema import MyGraphqlWsConsumer


application = channels.routing.ProtocolTypeRouter(
    {
        "http": django.core.asgi.get_asgi_application(),
        "websocket": channels.auth.AuthMiddlewareStack(
            channels.routing.URLRouter(
                [django.urls.path("subscriptions/", MyGraphqlWsConsumer.as_asgi())]
            )
        ),
    }
)
