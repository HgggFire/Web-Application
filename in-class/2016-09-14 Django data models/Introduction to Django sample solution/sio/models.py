from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    andrewId = models.CharField(max_length=100)

    def __unicode__(self):
        return self.andrewId

class Course(models.Model):
    courseNumber = models.IntegerField(max_length=10)
    courseName = models.CharField(max_length=300)
    instructor = models.CharField(max_length=200)

    def __unicode__(self):
        return self.courseNumber
