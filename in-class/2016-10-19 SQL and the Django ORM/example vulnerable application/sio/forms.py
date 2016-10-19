from django import forms
from sio.models import *

class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'instructor']

class RegisterStudentForm(forms.Form):
    andrew_id = forms.CharField(label='Andrew ID', max_length=20)
    course_number = forms.CharField(max_length=20)
    def clean(self):
        cleaned_data = super(RegisterStudentForm, self).clean()
        andrew_id = cleaned_data.get('andrew_id')
        course_number = cleaned_data.get('course_number')
        if andrew_id and Student.objects.filter(andrew_id=andrew_id).count() == 0:
            raise forms.ValidationError("%s is not a student"%andrew_id)
        if course_number and Course.objects.filter(course_number=course_number).count() == 0:
            raise forms.ValidationError("%s is not a course"%course_number)
        return cleaned_data
