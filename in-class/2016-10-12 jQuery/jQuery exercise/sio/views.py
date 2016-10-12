from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction

from sio.models import *
from sio.forms import *

import time
current_milli_time = lambda: int(round(time.time() * 1000))

def home(request):
    context = {'courses': Course.objects.all(),
               'create_student_form': CreateStudentForm(),
               'create_course_form': CreateCourseForm(),
               'register_student_form': RegisterStudentForm(),
               'timestamp': current_milli_time()
              }
    return render(request, 'sio.html', context)


@transaction.atomic
def create_student(request):
    messages = []
    try:
        timestamp = float(request.POST['timestamp'])
    except:
        timestamp = 0.0
    courses = Course.get_changes(timestamp)
    context = {'courses': courses, 'messages': messages, 'timestamp': current_milli_time()}

    form = CreateStudentForm(request.POST)
    if not form.is_valid():
        messages.append('Form contained invalid data')
        return render(request, 'courses.json', context, content_type='application/json')

    new_student = Student(andrew_id=form.cleaned_data['andrew_id'],
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'])
    new_student.save()
    messages.append('Added %s' % new_student)
    return render(request, 'courses.json', context, content_type='application/json')


@transaction.atomic
def create_course(request):
    messages = []
    try:
        timestamp = float(request.POST['timestamp'])
    except:
        timestamp = 0.0
    courses = Course.get_changes(timestamp)
    context = {'courses': courses, 'messages': messages, 'timestamp': current_milli_time()}

    form = CreateCourseForm(request.POST)
    if not form.is_valid():
        messages.append('Form contained invalid data')
        return render(request, 'courses.json', context, content_type='application/json')

    new_course = Course(course_number=form.cleaned_data['course_number'],
                        course_name=form.cleaned_data['course_name'],
                        instructor=form.cleaned_data['instructor'])
    new_course.save()
    messages.append('Added %s' % new_course)
    return render(request, 'courses.json', context, content_type='application/json')


@transaction.atomic
def register_student(request):
    messages = []
    try:
        timestamp = float(request.POST['timestamp'])
    except:
        timestamp = 0.0
    courses = Course.get_changes(timestamp)
    context = {'courses': courses, 'messages': messages, 'timestamp': current_milli_time()}

    form = RegisterStudentForm(request.POST)
    if not form.is_valid():
        messages.append("Form contained invalid data")
        return render(request, 'courses.json', context, content_type='application/json')

    course = Course.objects.get(course_number=form.cleaned_data['course_number'])
    student = Student.objects.get(andrew_id=form.cleaned_data['andrew_id'])
    course.students.add(student)
    course.save()
    messages.append('Added %s to %s' % (student, course))

    return render(request, 'courses.json', context, content_type='application/json')
