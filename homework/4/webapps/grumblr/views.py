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
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    followees = profile.followees.all()

    return render(request, 'grumblr/mainpage.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})


@login_required
def post(request):
    context = {}
    posts = Post.objects.all().order_by("-time")
    context['posts'] = posts
    context['user'] = request.user

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = PostForm()
        return render(request, 'grumblr/mainpage.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = PostForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/mainpage.html', context)


    # Creates a new item if it is present as a parameter in the request
    new_post = Post(post=form.cleaned_data['post'], user=request.user)
    new_post.save()

    posts = Post.objects.all().order_by("-time")
    context['posts'] = posts

    return render(request, 'grumblr/mainpage.html', context)

@login_required
def delete(request, id):
    errors = []

    # Deletes item if the logged-in user has an item matching the id
    try:
        item_to_delete = Post.objects.get(id=id, user=request.user)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        raise Http404

    # get the profile of the user
    try:
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    posts = Post.objects.filter(user=request.user).order_by('-time')
    context = {'posts' : posts, 'errors' : errors, 'profile' : user_profile}
    return render(request, 'grumblr/profile.html', context)


@login_required
def profile(request, username):
    try:
        post_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    # get the posts of the user specified
    posts_of_user = Post.objects.filter(user=post_user).order_by("-time")

    # get the profile of the user specified
    try:
        post_user_profile = Profile.objects.get(user=post_user)
    except ObjectDoesNotExist:
        raise Http404

    followees = request.user.profile.followees.all()

    context = {'posts' : posts_of_user, 'user' : post_user, 'profile' : post_user_profile, 'followees' : followees}
    return render(request, 'grumblr/profile.html', context)

@login_required
def follow(request, username):
    try:
        post_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    profile.followees.add(post_user);
    profile.save()

    followees = profile.followees.all()

    posts = Post.objects.filter(user__in=followees).order_by("-time")

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})

@login_required
def follower_stream(request, username):
    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    followees = profile.followees.all()

    posts = Post.objects.filter(user__in=followees).order_by("-time")

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})

@login_required
def unfollow(request, username):
    try:
        post_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    profile.followees.remove(post_user);
    profile.save()

    followees = profile.followees.all()

    posts = Post.objects.filter(user__in=followees).order_by("-time")

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'user' : request.user, 'followees' : followees})

@login_required()
def change_password(request):
    errors = []
    context = {}
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
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


    user = authenticate(username=user.username, \
                            password=user.password)
    login(request, user)

    context = {'posts' : posts, 'errors' : errors, 'user' : request.user, 'profile' : profile}
    return render(request, 'grumblr/profile.html', context)



@login_required
def edit_profile(request):
    print('editing')
    context = {}

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

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

    print('validated')
    # get the posts of the user specified
    posts_of_user = Post.objects.filter(user=request.user).order_by("-time")

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    # Make changes to the profile
    profile.age=form.cleaned_data['age']
    profile.bio=form.cleaned_data['bio']
    if form.cleaned_data['picture']:
        profile.picture=form.cleaned_data['picture']
    user = request.user
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    profile.save()
    request.user.save()

    context = {'posts' : posts_of_user, 'user' : request.user, 'profile' : profile}
    return render(request, 'grumblr/profile.html', context)


@login_required
def get_photo(request, username):
    # get the profile of the user specified
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404
    try:
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        raise Http404

    if not profile.picture:
        raise Http404
    content_type = guess_type(profile.picture.name)

    return HttpResponse(profile.picture, content_type=content_type)


@login_required
def go_edit(request):

    # get the profile of the user specified
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    context = {'profile' : profile}
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
    try:
        user= User.objects.get(email=form.cleaned_data['email'])
    except ObjectDoesNotExist:
        raise Http404

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
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

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

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = ChangePasswordForm(request.POST)
    context['form'] = form
    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/reset_password_form.html', context)

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404
    user.set_password(form.cleaned_data['password'])
    user.save()

    return redirect('/grumblr/mainpage')


@transaction.atomic
def registration_confirmation(request, username, token):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

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
