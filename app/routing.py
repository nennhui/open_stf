from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import screen.routing
import minitouch.routing
from django.conf.urls import url
from  screen.consumers import ChatConsumer as s
from  minitouch.consumers import ChatConsumer as f
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            # screen.routing.websocket_urlpatterns,
            # minitouch.routing.websocket_urlpatterns
            [ url(r'^ws/screen/(?P<room_name>[^/]+)/$',s ),
            url(r'^ws/minitouch/(?P<room_name>[^/]+)/$', f),]
        )
    ),

})