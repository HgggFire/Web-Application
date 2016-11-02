from django.test import TestCase, Client
from shared_todo_list.models import *

class TodoListModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(Item.objects.all().count() == 0)
        new_item = Item(text='A test item')
        new_item.save()
        self.assertTrue(Item.objects.all().count() == 1)
        self.assertTrue(Item.objects.filter(text__contains='test'))
        

class TodoListTest(TestCase):
                                # Seeds the test database with data we obtained
    fixtures = ['sample-data']  # from python manage.py dumpdata 


    def test_home_page(self):   # Tests that a GET request to /shared-todo-list/
        client = Client()       # results in an HTTP 200 (OK) response.
        response = client.get('/shared-todo-list/')
        self.assertEqual(response.status_code, 200)


    def test_add_item(self):    # Tests the to-do list add-item function.
        client = Client()       # add-item expects a POST request with one
                                # query parameter, item, the text of the to-do
                                # list item.
        sample_item = 'This is the text for my sample todo list item'
        response = client.post('/shared-todo-list/add-item', {'item':sample_item})
        self.assertTrue(response.content.find(sample_item.encode()) >= 0)



