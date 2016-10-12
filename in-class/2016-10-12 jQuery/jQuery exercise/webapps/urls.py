from django.conf.urls import url, include
from sio.views import home
from sio import urls

urlpatterns = [
    url(r'^sio/', include(urls)),
    url(r'^$', home),
]
