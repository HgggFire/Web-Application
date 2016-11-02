from django.conf.urls import url
from sio.views import *

urlpatterns = [
    url(r'^$', home),
    url(r'^home$', home),
    url(r'^create-student$', create_student),
    url(r'^create-course$', create_course),
    url(r'^register-student$', register_student),
]
