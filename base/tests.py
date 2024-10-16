# from django.test import TestCase

# # Create your tests here.
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from .models import Task

# class TaskTests(APITestCase):
#     def test_create_task(self):
#         url = reverse('task-list')
#         data = {'title': 'New Task', 'description': 'This is a new task.'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_task_creation(self):
        # Test creating a Task
        task = Task.objects.create(user=self.user, title='Test Task', description='Test Description', complete=False)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.complete, False)
        self.assertEqual(str(task), 'Test Task')  # Test the __str__ method

    def test_task_without_user(self):
        # Test creating a Task without a user
        task = Task.objects.create(title='Task without user', description='No user assigned', complete=False)
        self.assertEqual(task.title, 'Task without user')
        self.assertEqual(task.description, 'No user assigned')
        self.assertEqual(task.complete, False)
        self.assertEqual(str(task), 'Task without user')
