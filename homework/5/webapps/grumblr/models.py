from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.db.models import Max

# Create your models here.
class Post(models.Model):
    post = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.post

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(changetime="1970-01-01T00:00+00:00"):
        return Post.objects.filter(last_changed__gt=changetime).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_items(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(deleted=False,
                                   last_changed__gt=time).distinct()

    # Generates the HTML-representation of a single post item.
    @property
    def html(self):
        # return "<li id='item_%d'> <button class='delete-btn'>x</button> %s</li>" % (self.id, escape(self.text))

        # return "<p>%s</p>" % (self.post);
        return render_to_string("post.html", {"user":self.user,"post":self.post,"time":self.time,"post_id":self.id}).replace("\n", "");

    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"


class Profile(models.Model):
    age = models.PositiveSmallIntegerField()
    bio = models.CharField(max_length=420, default="Write your short bio here.", blank=True)
    user = models.OneToOneField(User, primary_key=True)
    picture = models.ImageField(upload_to="profile_pictures", blank=True)
    followees = models.ManyToManyField(
        User,
        related_name='User+',
    )

    @staticmethod
    def get_profile(user):
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            print('The profile does not exist.')

        return profile
