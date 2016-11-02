from django.conf.urls import include, url
from sio.views import home

urlpatterns = [
    url(r'^sio/', include('sio.urls')),
    url(r'^$', home),
]
