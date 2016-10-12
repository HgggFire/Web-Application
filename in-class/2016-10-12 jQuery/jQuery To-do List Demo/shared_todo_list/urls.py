from django.conf.urls import url

import shared_todo_list.views

urlpatterns = [
    url(r'^$', shared_todo_list.views.home),
    url(r'^add-item', shared_todo_list.views.add_item),
    url(r'^delete-item/(?P<item_id>\d+)$', shared_todo_list.views.delete_item),
    url(r'^get-items/?$', shared_todo_list.views.get_items),
    url(r'^get-items/(?P<time>.+)$', shared_todo_list.views.get_items),
    url(r'^get-changes/?$', shared_todo_list.views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', shared_todo_list.views.get_changes),
]

