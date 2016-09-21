from django.conf.urls import include, url

from shared_todo_list import views 

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add-item', views.add_item, name='home'),
    # Parses number from URL and uses it as the item_id argument to the action
    url(r'^delete-item/(?P<item_id>\d+)$', views.delete_item, name='delete-item')
]
