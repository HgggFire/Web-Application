from django.shortcuts import render
from django.db import transaction

from sio.models import *

def home(request):
    context = {'courses':Course.objects.all(), 'messages':[]}
    return render(request, 'sio.html', context)

@transaction.atomic
def create_student(request):
    messages = []
    context = {'courses':Course.objects.all(), 'messages':messages}
    
    if not 'andrew_id' in request.POST or not request.POST['andrew_id']:
        messages.append("Andrew ID is required.")
    elif Student.objects.filter(andrew_id=request.POST['andrew_id']).count() > 0:
        messages.append("A student with Andrew ID %s already exists." % 
                      request.POST['andrew_id'])
    if not 'first_name' in request.POST or not request.POST['first_name']:
        messages.append("First name is required.")
    if not 'last_name' in request.POST or not request.POST['last_name']:
        messages.append("Last name is required.")

    if messages:
        return render(request, 'sio.html', context)

    new_student = Student(andrew_id=request.POST['andrew_id'],
                          first_name=request.POST['first_name'],
                          last_name=request.POST['last_name'])
    new_student.save()

    messages.append('Added %s' % new_student)
    return render(request, 'sio.html', context)

@transaction.atomic
def create_course(request):
    messages = []
    context = {'courses':Course.objects.all(), 'messages':messages}

    if not 'course_number' in request.POST or not request.POST['course_number']:
        messages.append("Course number is required.")
    elif Course.objects.filter(course_number=request.POST['course_number']).count() > 0:
        messages.append("Course %s already exists." % 
                      request.POST['course_number'])
    if not 'course_name' in request.POST or not request.POST['course_name']:
        messages.append("Course name is required.")
    if not 'instructor' in request.POST or not request.POST['instructor']:
        messages.append("Instructor is required.")

    if messages:
        return render(request, 'sio.html', context)

    new_course = Course(course_number=request.POST['course_number'],
                        course_name=request.POST['course_name'],
                        instructor=request.POST['instructor'])
    new_course.save()

    messages.append('Added %s' % new_course)
    return render(request, 'sio.html', context)

@transaction.atomic
def register_student(request):
    messages = []
    context = {'courses':Course.objects.all(), 'messages':messages}

    if not 'andrew_id' in request.POST or not request.POST['andrew_id']:
        messages.append("Andrew ID is required.")
    elif Student.objects.filter(andrew_id=request.POST['andrew_id']).count() != 1:
        messages.append("Could not find Andrew ID %s." %
                        request.POST['andrew_id'])
    if not 'course_number' in request.POST or not request.POST['course_number']:
        messages.append("Course number is required.")
    elif Course.objects.filter(course_number=request.POST['course_number']).count() != 1:
        messages.append("Could not find course %s." %
                        request.POST['course_number'])

    if messages:
        return render(request, 'sio.html', context)

    course = Course.objects.get(course_number=request.POST['course_number'])
    student = Student.objects.get(andrew_id=request.POST['andrew_id'])
    course.students.add(student)
    course.save()

    messages.append('Added %s to %s' % (student, course))
    return render(request, 'sio.html', context)
