from channels.routing import route
from private_todo_list.consumers import ws_message, ws_connect, ws_disconnect

channel_routing = [
    ## Route http requests to consumers.http_consumer
    # route("http.request", "private_todo_list.consumers.http_consumer"),

    route("websocket.connect", ws_connect, path=r"^/(?P<room>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
