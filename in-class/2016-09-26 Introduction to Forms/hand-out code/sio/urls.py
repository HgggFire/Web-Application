from django.conf.urls import include, url
from sio.views import home, create_student, create_course, register_student

urlpatterns = [
    url(r'^$', home),
    url(r'^home$', home),
    url(r'^create-student$', create_student, name="create_student"),
    url(r'^create-course$', create_course, name="create_course"),
    url(r'^register-student$', register_student, name="register_student"),
]
