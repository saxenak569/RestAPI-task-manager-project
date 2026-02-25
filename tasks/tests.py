from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken


class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='shiv',
            password='saxena@kk'
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Set Authorization header
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

    def test_create_task(self):
        response = self.client.post('/api/tasks/', {
            'title': 'Test Task',
            'description': 'Test Description',
            'completed': False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks(self):
        Task.objects.create(
            user=self.user,
            title='Task1',
            description='Desc',
            completed=False
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)