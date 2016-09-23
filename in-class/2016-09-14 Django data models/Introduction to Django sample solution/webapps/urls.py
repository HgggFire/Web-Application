from django.conf.urls import url
import sio.views

urlpatterns = [
    url(r'^$', sio.views.home),
    #  will add routes later for add student / add course / register actions
    url(r'^/sio/create-student', sio.views.createStudent),
    url(r'^/sio/create-course', sio.views.createCourse),
    url(r'^/sio/register', sio.views.register),
]
