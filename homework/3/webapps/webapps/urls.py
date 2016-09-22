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
from django.contrib import admin

from django.conf.urls import include, url

import django.contrib.auth.views

import grumblr.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', grumblr.views.home),
    url(r'^grumblr$', grumblr.views.home),
    url(r'^grumblr/post', grumblr.views.post, name='post'),
    url(r'^grumblr/profile/(?P<id>\d+)$', grumblr.views.profile),
    # Route for built-in authentication with our own custom login page
    url(r'^grumblr/login$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^grumblr/logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^grumblr/register$', grumblr.views.register, name='register'),
    url(r'^grumblr/mainpage$', grumblr.views.home, name='home'),
]
