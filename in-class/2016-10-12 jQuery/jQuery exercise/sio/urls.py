from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home$', views.home),
    url(r'^create-student$', views.create_student),
    url(r'^create-course$', views.create_course),
    url(r'^register-student$', views.register_student),
]
