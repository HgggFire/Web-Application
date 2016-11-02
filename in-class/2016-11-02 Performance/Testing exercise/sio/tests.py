from django.test import TestCase, Client
from sio.models import *
# Create your tests here.

class SioModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(Student.objects.all().count() == 0)
        new_student = Student(andrew_id='jiumings', first_name='Jason', last_name='Shao')
        new_student.save()
        self.assertTrue(Student.objects.all().count() == 1)
        self.assertTrue(Student.objects.filter(andrew_id='jiumings'))

        # self.assertTrue(Course.objects.all().count() == 0)
        # new_course = Course(andrew_id='jiumings', first_name='Jason', last_name='Shao')
        # new_course.save()
        # self.assertTrue(Course.objects.all().count() == 1)
        # self.assertTrue(Course.objects.filter(andrew_id='jiumings'))


class SioTest(TestCase):
                                # Seeds the test database with data we obtained
    fixtures = ['sample-data']  # from python manage.py dumpdata


    def test_home_page(self):   # Tests that a GET request to /shared-todo-list/
        client = Client()       # results in an HTTP 200 (OK) response.
        response = client.get('/sio/')
        self.assertEqual(response.status_code, 200)


    def test_add_item(self):    # Tests the to-do list add-item function.
        client = Client()       # add-item expects a POST request with one
                                # query parameter, item, the text of the to-do
                                # list item.

        response = client.post('/sio/create-student', {'andrew_id':'jiet', 'first_name':'Jess', 'last_name':'Tan'})
        self.assertTrue(response.content.find('jiet'.encode()) >= 0)
