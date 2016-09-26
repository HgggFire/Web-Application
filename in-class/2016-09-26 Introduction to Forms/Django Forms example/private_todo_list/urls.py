from django.conf.urls import include, url
from private_todo_list import views
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add-item', views.add_item, name='add'),
    url(r'^delete-item/(?P<id>\d+)$', views.delete_item, name='delete'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', login, {'template_name':'private-todo-list/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
]
