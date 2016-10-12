from django.conf.urls import include, url

import shared_todo_list.views

urlpatterns = [
    url(r'^shared-todo-list/', include('shared_todo_list.urls')),
    url(r'^$', shared_todo_list.views.home),
]
