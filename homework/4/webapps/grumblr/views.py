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
from mimetypes import guess_type

from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse

from django.core.mail import send_mail
from django.db import transaction

@login_required
def home(request):
    # Sets up list of all the users' items
    posts = Post.objects.all().order_by("-time")

    profile = Profile.objects.get(user=request.user)
    followees = profile.followees.all()

    return render(request, 'grumblr/mainpage.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})


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

    context = {'posts' : posts_of_user, 'errors' : errors, 'user' : post_user, 'profile' : profile}
    return render(request, 'grumblr/profile.html', context)

@login_required
def follow(request, username):
    errors = []

    post_user = User.objects.get(username=username)

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    profile.followees.add(post_user);
    profile.save()

    followees = profile.followees.all()

    posts = Post.objects.filter(user__in=followees).order_by("-time")

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})

@login_required
def follower_stream(request, username):
    errors = []

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    followees = profile.followees.all()

    posts = Post.objects.filter(user__in=followees).order_by("-time")

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})

@login_required
def unfollow(request, username):
    errors = []

    post_user = User.objects.get(username=username)

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        errors.append('The profile did not exist.')

    profile.followees.remove(post_user);
    profile.save()

    followees = profile.followees.all()

    posts = Post.objects.filter(user__in=followees).order_by("-time")

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})

@login_required()
def change_password(request):
    errors = []
    context = {}
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
        context['profile'] = profile
        return render(request, 'grumblr/edit_profile.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = ChangePasswordForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context['profile'] = profile
        return render(request, 'grumblr/edit_profile.html', context)

    # Change the password of the user
    user = request.user
    user.set_password(form.cleaned_data['password'])
    user.save()

    # get the posts of the user specified
    posts = Post.objects.filter(user=request.user).order_by("-time")

    context = {'posts' : posts, 'errors' : errors, 'user' : request.user, 'profile' : profile}
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
        print("not valid\n")
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
    if form.cleaned_data['picture']:
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

@transaction.atomic
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
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        is_active=False)
    new_user.save()


    token = default_token_generator.make_token(new_user)

    email_body="""
    Welcome to Grumblr! Please click the link below to verify
    your email address and complete the registration of your account:
    http://%s%s
    """ % (request.get_host(),
           reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Grumblr - Verify your email address",
              message=email_body,
              from_email="chicolin@cs.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'grumblr/email_confirmation.html', context)

@transaction.atomic
def go_reset(request):
    return render(request, 'grumblr/reset_password.html')

@transaction.atomic
def reset_password(request):
    context = {}
    if request.method == 'GET':
        context['form'] = EmailResetForm()
        return render(request, 'grumblr/reset_password.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = EmailResetForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/reset_password.html', context)

    user= User.objects.get(email=form.cleaned_data['email'])

    token = default_token_generator.make_token(user)

    email_body="""
    Please click the link below to verify your email address
    and complete the password resetting of your account:
    http://%s%s
    """ % (request.get_host(),
           reverse('password_confirm', args=(user.username, token)))

    send_mail(subject="Grumblr - Verify your email address",
              message=email_body,
              from_email="chicolin@cs.cmu.edu",
              recipient_list=[user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'grumblr/reset_email_confirmation.html', context)

@transaction.atomic
def password_reset_confirmation(request, username, token):
    context = {}
    user = User.objects.get(username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    context['user'] = user
    # # Logs in the new user and redirects to mainpage
    # user = authenticate(username=user.username, \
    #                         password=user.password)
    return render(request, 'grumblr/reset_password_form.html', context)

@transaction.atomic
def password_reset_form(request, username):
    context = {}
    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
        return render(request, 'grumblr/reset_password_form.html', context)
    print("\n1\n")

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = ChangePasswordForm(request.POST)
    context['form'] = form
    print("\n2\n")
    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/reset_password_form.html', context)

    print("\n3\n")
    user = User.objects.get(username=username)
    user.set_password(form.cleaned_data['password'])
    user.save()

    return redirect('/grumblr/mainpage')


@transaction.atomic
def registration_confirmation(request, username, token):
    user = User.objects.get(username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active=True
    user.save()

    # create a default profile for the user
    new_profile = Profile(age=0, user=user, bio='Write your short bio here.')
    new_profile.save()

    # # Logs in the new user and redirects to mainpage
    # user = authenticate(username=user.username, \
    #                         password=user.password)
    login(request, user)

    return redirect('/grumblr/mainpage')