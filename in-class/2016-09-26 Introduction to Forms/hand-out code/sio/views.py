from django.shortcuts import render
from django.db import transaction

from sio.models import *
from sio.forms import *

def home(request):
    context = {'courses':Course.objects.all()}

    forms = {'studentForm':CreateStudentForm(),
             'courseForm':CreateCourseForm(),
             'registrationForm':RegistrationForm()}
    context['forms'] = forms

    return render(request, 'sio.html', context)

@transaction.atomic
def create_student(request):
    context = {'courses':Course.objects.all()}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        forms = {'studentForm':CreateStudentForm(),
                 'courseForm':CreateCourseForm(),
                 'registrationForm':RegistrationForm()}
        context['forms'] = forms

        return render(request, 'sio.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = CreateStudentForm(request.POST)
    forms = {'studentForm':form,
             'courseForm':CreateCourseForm(),
             'registrationForm':RegistrationForm()}
    context['forms'] = forms

    # Validates the form.
    if not form.is_valid():
        return render(request, 'sio.html', context)

    new_student = Student(andrew_id=form.cleaned_data['andrew_id'],
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'])
    new_student.save()

    return render(request, 'sio.html', context)

@transaction.atomic
def create_course(request):
    context = {'courses':Course.objects.all()}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        forms = {'studentForm':CreateStudentForm(),
                 'courseForm':CreateCourseForm(),
                 'registrationForm':RegistrationForm()}
        context['forms'] = forms

        return render(request, 'sio.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = CreateCourseForm(request.POST)
    forms = {'studentForm':CreateStudentForm(),
             'courseForm':form,
             'registrationForm':RegistrationForm()}
    context['forms'] = forms

    # Validates the form.
    if not form.is_valid():
        return render(request, 'sio.html', context)

    new_course = Course(course_number=form.cleaned_data['course_num'],
                        course_name=form.cleaned_data['course_name'],
                        instructor=form.cleaned_data['instructor'])
    new_course.save()

    return render(request, 'sio.html', context)

@transaction.atomic
def register_student(request):
    context = {'courses':Course.objects.all()}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        forms = {'studentForm':CreateStudentForm(),
                 'courseForm':CreateCourseForm(),
                 'registrationForm':RegistrationForm()}
        context['forms'] = forms

        return render(request, 'sio.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    forms = {'studentForm':CreateStudentForm(),
             'courseForm':CreateCourseForm(),
             'registrationForm':form}
    context['forms'] = forms

    # Validates the form.
    if not form.is_valid():
        return render(request, 'sio.html', context)

    course = Course.objects.get(course_number=form.cleaned_data['course_num'])
    student = Student.objects.get(andrew_id=form.cleaned_data['andrew_id'])
    course.students.add(student)
    course.save()

    return render(request, 'sio.html', context)
