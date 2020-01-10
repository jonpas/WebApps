from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import doodle.consumers
import ludo.consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'ws/doodle/(?P<room_id>\w+)/$', doodle.consumers.ChatConsumer),
            url(r'ws/ludo/(?P<room_id>\w+)/$', ludo.consumers.GameConsumer),
        ])
    ),
})
