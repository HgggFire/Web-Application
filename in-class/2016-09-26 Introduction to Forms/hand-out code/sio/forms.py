from django import forms

from django.contrib.auth.models import User

from sio.models import *

class CreateStudentForm(forms.Form):
    andrew_id = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 40)
    last_name = forms.CharField(max_length = 40)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(CreateStudentForm, self).clean()

        # Confirms that the andrewId is not already present in the
        # Student model database.
        andrewId = self.cleaned_data.get('andrew_idd')
        if Student.objects.filter(andrew_id=andrewId):
            raise forms.ValidationError("AndrewID is already taken.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


class CreateCourseForm(forms.Form):
    course_num = forms.IntegerField()
    course_name = forms.CharField(max_length = 255)
    instructor = forms.CharField(max_length = 255)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(CreateCourseForm, self).clean()

        # Confirms that the course number is not already present in the
        # Course model database.
        courseNum = self.cleaned_data.get('course_num')
        if Course.objects.filter(course_number=courseNum):
            raise forms.ValidationError("Course Number is already taken.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class RegistrationForm(forms.Form):
    course_num = forms.IntegerField()
    andrew_id = forms.CharField(max_length = 20)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the course number and andrewId exist in the database
        courseNum = self.cleaned_data.get('course_num')
        if not Course.objects.filter(course_number=courseNum):
            raise forms.ValidationError("Course does not exist.")

        andrewId = self.cleaned_data.get('andrew_id')
        if not Student.objects.filter(andrew_id=andrewId):
            raise forms.ValidationError("Student does not exist.")

        # Confirms that the student haven't registered for this course before
        course = Course.objects.get(course_number=courseNum)
        if course.students.filter(andrew_id=andrewId):
            raise forms.ValidationError("Student " + andrewId + " is already registered to the course " + str(courseNum) + ".")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data