"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url

import django.contrib.auth.views


import grumblr.views

urlpatterns = [
    url(r'^$', grumblr.views.home),
    url(r'^post', grumblr.views.post, name='post'),
    url(r'^profile/(?P<username>\w+)$', grumblr.views.profile, name='profile'),
    url(r'^photo/(?P<username>\w+)$', grumblr.views.get_photo, name='photo'),
    url(r'^follow/(?P<username>\w+)$', grumblr.views.follow, name='follow'),
    url(r'^follower_stream/(?P<username>\w+)$', grumblr.views.follower_stream, name='follower_stream'),
    url(r'^unfollow/(?P<username>\w+)$', grumblr.views.unfollow, name='unfollow'),
    url(r'^password_reset_form/(?P<username>\w+)$', grumblr.views.password_reset_form, name='reset_form'),
    url(r'^go_edit$', grumblr.views.go_edit, name='go_edit'),
    url(r'^edit_profile$', grumblr.views.edit_profile, name='edit_profile'),
    url(r'^go_reset$', grumblr.views.go_reset, name='go_reset'),
    url(r'^reset_password$', grumblr.views.reset_password, name='reset_password'),
    url(r'^change_password$', grumblr.views.change_password, name='change_password'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    # url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^mainpage$', grumblr.views.home, name='home'),
    url(r'^delete/(?P<id>\d+)$', grumblr.views.delete, name='delete'),
    url(r'^registration_confirmation/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', grumblr.views.registration_confirmation, name='confirm'),
    url(r'^password_reset_confirmation/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', grumblr.views.password_reset_confirmation, name='password_confirm'),
    url(r'^get-changes/(?P<time>.+)$', grumblr.views.get_changes),
    url(r'^get-changes/?$', grumblr.views.get_changes),
]
