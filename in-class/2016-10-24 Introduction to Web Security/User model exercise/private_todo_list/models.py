from django.db import models
from django.contrib.auth.models import BaseUserManager
import hashlib, random

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        u = User(username=username)
        u.set_password(password)
        return u
    def create_superuser(self, username, password):
        return self.create_user(username, password)

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateField(auto_now_add=True)
    salt = models.CharField(max_length=42,default='mysalt')

    def set_password(self, password):
        salt = str(random.randrange(9999999))
        self.salt = salt;
        hash_obj = hashlib.sha256()
        hash_obj.update(password + salt)
        self.password = hash_obj.hexdigest()
        # TODO: Very insecure! Stores password in clear-text.

    def check_password(self, password):
        salt = self.salt;
        hash_obj = hashlib.sha256()
        hash_obj.update(password + salt)
        hashed_password = hash_obj.hexdigest()
        return hashed_password == self.password # Check user-typed password vs. stored password.

    def __unicode__(self):
        return self.username
    def __str__(self):
        return self.__unicode__()

    # These fields and methods are necessary to use this model with
    # the rest of the Django authentication framework
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()
    is_anonymous = False
    is_authenticated = True
    is_active = True
    def get_short_name(self):
        return self.username
    def get_long_name(self):
        return self.username

class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()
