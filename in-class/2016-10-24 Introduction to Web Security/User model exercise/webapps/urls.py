from django.conf.urls import include, url
import private_todo_list.views

urlpatterns = [
    url(r'^private-todo-list/', include('private_todo_list.urls')),
    url(r'^$', private_todo_list.views.home),
]
