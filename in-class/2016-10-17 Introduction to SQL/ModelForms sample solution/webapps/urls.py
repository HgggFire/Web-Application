from django.conf.urls import include, url

import sio.views

urlpatterns = [
    url(r'^sio/', include('sio.urls')),
    url(r'^$', sio.views.home),
]
