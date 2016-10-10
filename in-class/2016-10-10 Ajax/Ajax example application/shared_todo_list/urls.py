from django.conf.urls import include, url

import shared_todo_list.views

urlpatterns = [
    url(r'^$', shared_todo_list.views.home),
    url(r'^add-item', shared_todo_list.views.add_item),
    url(r'^delete-item/(?P<item_id>\d+)$', shared_todo_list.views.delete_item),
    url(r'^get-list$', shared_todo_list.views.get_list),
]
