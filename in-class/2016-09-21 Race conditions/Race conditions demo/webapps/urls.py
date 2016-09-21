from django.conf.urls import include, url

from shared_todo_list import views 

urlpatterns = [
    url(r'^shared-todo-list/', include('shared_todo_list.urls')),
    url(r'^$', views.home, name='home'),
]
