from django.conf.urls import include, url

import sio.views

urlpatterns = [
    url(r'^sio/', include('sio.urls')),
    url(r'^sio/get-all-courses', sio.views.get_all_courses),
    url(r'^$', sio.views.home),
]
