from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text