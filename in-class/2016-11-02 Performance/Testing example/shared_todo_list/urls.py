from django.conf.urls import url
from shared_todo_list.views import *

urlpatterns = [
    url(r'^$', home),
    url(r'^add-item', add_item),
    url(r'^delete-item/(?P<item_id>\d+)$', delete_item),
]
