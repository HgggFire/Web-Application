from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from private_todo_list.views import *

urlpatterns = [
    url(r'^$', home),
    url(r'^add-item', add_item),
    url(r'^delete-item/(?P<id>\d+)$', delete_item),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', login, {'template_name':'private-todo-list/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^register$', register),
]
