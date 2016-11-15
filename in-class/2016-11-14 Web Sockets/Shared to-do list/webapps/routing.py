# In routing.py
# In routing.py
from channels.routing import route
from shared_todo_list.consumers import ws_message

channel_routing = [
    route("websocket.receive", ws_message),
]
