from django.db import models
from django.db.models import Max
from django.utils.html import escape

class Item(models.Model):
    text = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Item.objects.filter(last_changed__gt=time).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_items(time="1970-01-01T00:00+00:00"):
        return Item.objects.filter(deleted=False,
                                   last_changed__gt=time).distinct()

    # Generates the HTML-representation of a single to-do list item.
    @property
    def html(self):
        return "<li id='item_%d'> <button class='delete-btn'>x</button> %s</li>" % (self.id, escape(self.text))

    @staticmethod
    def get_max_time():
        return Item.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"
