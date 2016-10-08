# Create your views here.
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *
from grumblr.forms import *

from django.http import HttpResponse, Http404

from mimetypes import  guess_type

@login_required
def home(request):
    # Sets up list of all the users' items
    posts = Post.objects.all().order_by("-time")
    return render(request, 'grumblr/mainpage.html', {'posts' : posts, 'user' : request.user})


@login_required
def post(request):
    errors = []

    # Creates a new item if it is present as a parameter in the request
    if not 'post' in request.POST or not request.POST['post']:
        errors.append('You must enter an item to add.')
    else:
        new_post = Post(post=request.POST['post'], user=request.user)
        new_post.save()

    posts = Post.objects.all().order_by("-time")

    context = {'posts' : posts, 'errors' : errors, 'user' : request.user}
    return render(request, 'grumblr/mainpage.html', context)

@login_required
def delete(request, id):
    errors = []

    # Deletes item if the logged-in user has an item matching the id
    try:
        item_to_delete = Post.objects.get(id=id, user=request.user)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The item did not exist in your todo list.')

    posts = Post.objects.filter(user=request.user).order_by('-time')
    context = {'posts' : posts, 'errors' : errors}
    return render(request, 'grumblr/profile.html', context)


@login_required
def profile(request, username):
    errors = []

    post_user = User.objects.get(username=username)

    # get the posts of the user specified
    posts_of_user = Post.objects.filter(user=post_user).order_by("-time")

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=post_user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    print(profile.picture.name + "\n")

    context = {'posts' : posts_of_user, 'errors' : errors, 'user' : post_user, 'profile' : profile}
    return render(request, 'grumblr/profile.html', context)

@login_required
def edit_profile(request):
    errors = []
    context = {}

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    # Just display the form if this is a GET request
    if request.method == 'GET':
        context['form'] = EditProfileForm()
        context['profile'] = profile
        return render(request, 'grumblr/edit_profile.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = EditProfileForm(request.POST, request.FILES)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context['profile'] = profile
        return render(request, 'grumblr/edit_profile.html', context)

    # get the posts of the user specified
    posts_of_user = Post.objects.filter(user=request.user).order_by("-time")

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    # Make changes to the profile
    profile.age=form.cleaned_data['age']
    profile.bio=form.cleaned_data['bio']
    profile.picture=form.cleaned_data['picture']
    user = request.user
    user.first_name = form.cleaned_data['first_name']
    print(form.cleaned_data['first_name'])
    user.last_name = form.cleaned_data['last_name']
    profile.save()
    request.user.save()

    context = {'posts' : posts_of_user, 'errors' : errors, 'user' : request.user, 'profile' : profile}
    return render(request, 'grumblr/profile.html', context)


@login_required
def get_photo(request, username):
    print("getting photo\n")
    # get the profile of the user specified
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    if not profile.picture:
        raise Http404
    content_type = guess_type(profile.picture.name)

    return HttpResponse(profile.picture, content_type=content_type)


@login_required
def go_edit(request):
    errors = []

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    context = {'errors' : errors, 'profile' : profile}
    return render(request, 'grumblr/edit_profile.html', context)

def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'grumblr/signup.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/signup.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password'], \
                                        first_name=form.cleaned_data['first_name'], \
                                        last_name=form.cleaned_data['last_name'],)
    new_user.save()

    # create a default profile for the user
    new_profile = Profile(age=0, user=new_user, bio='Write your short bio here.')
    new_profile.save()
    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'], \
                            password=form.cleaned_data['password'])
    login(request, new_user)

    return redirect('/grumblr/mainpage')

