from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from time import sleep

# Imports the Item class
from shared_todo_list.models import *


# Action for the default shared-todo-list/ route.
def home(request):
    # Gets a list of all the items in the todo-list database.
    all_items = Item.objects.all()

    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    return render(request, 'shared-todo-list/index.html', {'items':all_items})


# Action for the shared-todo-list/add-item route.
def add_item(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must enter an item to add.')
    else:
        new_item = Item(text=request.POST['item'])
        new_item.save()

    # Added sleep call to better demonstrate an existing race condition
    sleep(5)

    # Sets up data needed to generate the view, and generates the view
    items = Item.objects.all()
    context = {'items':items, 'errors':errors}
    return render(request, 'shared-todo-list/index.html', context)
    
# Action for the shared-todo-list/delete-item route.
def delete_item(request, item_id):
    errors = []

    # Deletes the item if present in the todo-list database.
    try:
        item_to_delete = Item.objects.get(id=item_id)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The item did not exist in the todo list.')

    # Added sleep call to better demonstrate an existing race condition
    sleep(5)

    items = Item.objects.all()
    context = {'items':items, 'errors':errors}
    return render(request, 'shared-todo-list/index.html', context)