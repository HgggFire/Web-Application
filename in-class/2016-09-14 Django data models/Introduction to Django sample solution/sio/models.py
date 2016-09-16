from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    andrewId = models.CharField(max_length=100)

    def __str__(self):
        return self.andrewId

    class Meta:
        ordering = ('andrewId',)


class Course(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField()
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)