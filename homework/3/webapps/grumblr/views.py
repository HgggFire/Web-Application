# Create your views here.
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *


@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    items = Item.objects.filter(user=request.user)
    return render(request, 'grumblr/mainpage.html', {'items' : items})


@login_required
def post(request):
    errors = []

    # Creates a new item if it is present as a parameter in the request
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must enter an item to add.')
    else:
        new_item = Item(text=request.POST['item'], user=request.user)
        new_item.save()

    items = Item.objects.filter(user=request.user)
    context = {'items' : items, 'errors' : errors}
    return render(request, 'grumblr/mainpage.html', context)


@login_required
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


def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'grumblr/signup.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First name is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['firstname'] = request.POST['firstname']

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last name is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['lastname'] = request.POST['lastname']

    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if 'username' in request.POST and len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'grumblr/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/grumblr/mainpage.html')

