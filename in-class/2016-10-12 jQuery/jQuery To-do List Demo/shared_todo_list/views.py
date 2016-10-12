from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie

from shared_todo_list.models import *

@ensure_csrf_cookie  # Gives CSRF token for later requests.
def home(request):
    return render(request, 'index.html', {})


def add_item(request):
    if not 'item' in request.POST or not request.POST['item']:
        raise Http404
    else:
        new_item = Item(text=request.POST['item'])
        new_item.save()

    return HttpResponse("")  # Empty response on success.
    

def delete_item(request, item_id):
    try:
        item_to_delete = Item.objects.get(id=item_id)
        item_to_delete.deleted = True  # Just mark items as deleted.
        item_to_delete.save()
    except ObjectDoesNotExist:
        return HttpResponse("The item did not exist")

    return HttpResponse("")  # Empty response on success.


# Returns all recent additions in the database, as JSON
def get_items(request, time="1970-01-01T00:00+00:00"):
    max_time = Item.get_max_time()
    items = Item.get_items(time)
    context = {"max_time":max_time, "items":items}
    return render(request, 'items.json', context, content_type='application/json')
    

# Returns all recent changes to the database, as JSON
def get_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Item.get_max_time()
    items = Item.get_changes(time)
    context = {"max_time":max_time, "items":items} 
    return render(request, 'items.json', context, content_type='application/json')
    
