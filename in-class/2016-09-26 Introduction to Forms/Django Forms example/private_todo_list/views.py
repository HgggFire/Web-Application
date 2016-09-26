from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from private_todo_list.models import *
from private_todo_list.forms import *


@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    items = Item.objects.filter(user=request.user) 
    return render(request, 'private-todo-list/index.html', {'items' : items})


@login_required
@transaction.atomic
def add_item(request):
    errors = []

    # Creates a new item if it is present as a parameter in the request
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must enter an item to add.')
    else:
        new_item = Item(text=request.POST['item'], user=request.user)
        new_item.save()

    items = Item.objects.filter(user=request.user)
    context = {'items' : items, 'errors' : errors}
    return render(request, 'private-todo-list/index.html', context)
    

@login_required
@transaction.atomic
def delete_item(request, id):
    errors = []

    # Deletes item if the logged-in user has an item matching the id
    try:
        item_to_delete = Item.objects.get(id=id, user=request.user)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The item did not exist in your todo list.')

    items = Item.objects.filter(user=request.user)
    context = {'items' : items, 'errors' : errors}
    return render(request, 'private-todo-list/index.html', context)


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'private-todo-list/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'private-todo-list/register.html', context)

    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'], \
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect('/private-todo-list/')
    
