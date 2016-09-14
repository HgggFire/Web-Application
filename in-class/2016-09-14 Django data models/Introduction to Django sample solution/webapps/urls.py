from django.conf.urls import url
import sio.views

urlpatterns = [
    url(r'^$', sio.views.home),
    #  will add routes later for add student / add course / register actions
]
