from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Lesson, Course, Subscription

class CRUDLessonTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.moderator = User.objects.create_superuser(email='moderator@example.com', password='moderatorpassword')
        self.course = Course.objects.create(title='Test Course', description='Test Course Description', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson Description', video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', course=self.course, owner=self.user)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'course': self.course.id
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Lesson Title'}
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

class SubscriptionTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.course = Course.objects.create(title='Test Course', description='Test Course Description', owner=self.user)

    def test_add_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/subscriptions/', {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Subscription added"})
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/subscriptions/', {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Subscription removed"})
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
