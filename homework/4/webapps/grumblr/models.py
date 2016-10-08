from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    post = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.post

class Profile(models.Model):
    age = models.PositiveSmallIntegerField()
    bio = models.CharField(max_length=420)
    user = models.ForeignKey(User, primary_key=True)