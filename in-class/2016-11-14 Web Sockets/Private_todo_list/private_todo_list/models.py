from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()

