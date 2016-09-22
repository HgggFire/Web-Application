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
    posts = Post.objects.filter(user=request.user)
    return render(request, 'grumblr/mainpage.html', {'posts' : posts})


@login_required
def post(request):
    errors = []

    # Creates a new item if it is present as a parameter in the request
    if not 'post' in request.POST or not request.POST['post']:
        errors.append('You must enter an item to add.')
    else:
        new_post = Post(post=request.POST['post'], user=request.user)
        new_post.save()

    posts = Post.objects.all()
    postsList = list(posts)
    postsList.reverse()
    name = request.user.first_name + " " + request.user.last_name

    context = {'posts' : postsList, 'errors' : errors, 'user_name' : name}
    return render(request, 'grumblr/mainpage.html', context)


@login_required
def profile(request, id):
    errors = []

    post_clicked = Post.objects.get(id=id)
    post_user = post_clicked.user

    # get the posts of the user specified
    posts_of_user = Post.objects.filter(user=post_user)

    context = {'posts' : posts_of_user, 'errors' : errors}
    return render(request, 'grumblr/profile.html', context)


def register(request):
    print('\n1')
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'grumblr/signup.html', context)

    errors = []
    context['errors'] = errors
    print('\n2')
    # Checks the validity of the form data
    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First name is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['firstname'] = request.POST['firstname']
    print('\n3')

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last name is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['lastname'] = request.POST['lastname']
    print('\n4')
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']
    print('\n5')
    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')
    print('\n6')
    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if 'username' in request.POST and len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')
    print('\n7')
    if errors:
        return render(request, 'grumblr/signup.html', context)
    print('\n8')
    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'], \
                                        first_name=request.POST['firstname'], \
                                        last_name=request.POST['lastname'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    login(request, new_user)

    print('\nend\n')
    return redirect('/grumblr/mainpage')

