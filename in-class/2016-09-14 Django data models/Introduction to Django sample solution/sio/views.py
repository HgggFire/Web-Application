from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'sio.html', {})

def createStudent(request):
    errors = [] # A list to record messages for any errors we encounter.

    # Adds the new student to the database if the request parameter is present
    if not 'first-name' in request.POST or not request.POST['first-name']:
        errors.append('You must enter your first name to add.')
    elif not 'last-name' in request.POST or not request.POST['last-name']:
        errors.append('You must enter your last name to add.')
    elif not 'andrew-id' in request.POST or not request.POST['andrew-id']:
        errors.append('You must enter your AndrewID to add.')
    else:
        new_student = Student(firstName=request.POST['first-name'], lastName=request.POST['last-name'], andrewId=request.POST['andrew-id'])
        new_student.save()

    # Sets up data needed to generate the view, and generates the view
    students = Student.objects.all()
    context = {'students':students, 'errors':errors}

    return render(request, 'sio.html', context)

def createCourse(request):
    errors = [] # A list to record messages for any errors we encounter.

    # Adds the new student to the database if the request parameter is present
    if not 'course-number' in request.POST or not request.POST['course-number']:
        errors.append('You must enter the course number to add.')
    elif not 'course-name' in request.POST or not request.POST['course-name']:
        errors.append('You must enter the course name to add.')
    elif not 'instructor' in request.POST or not request.POST['instructor']:
        errors.append('You must enter the instructor to add.')
    else:
        new_course = Course(courseNumber=request.POST['course-number'], courseName=request.POST['course-name'], instructor=request.POST['instructor'])
        new_course.save()

    # Sets up data needed to generate the view, and generates the view
    courses = Course.objects.all()
    context = {'courses':courses, 'errors':errors}

    return render(request, 'sio.html', context)

def register(request):
    return render(request, 'sio.html', {})
