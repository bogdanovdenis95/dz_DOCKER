import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from lms.models import Course, Lesson
from users.models import User  # Используйте вашу кастомную модель User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(email='user@example.com', password='password')

@pytest.fixture
def moderator_group():
    return Group.objects.create(name='Модераторы')

@pytest.fixture
def moderator(moderator_group):
    user = User.objects.create_user(email='moderator@example.com', password='password')
    user.groups.add(moderator_group)
    return user

@pytest.fixture
def course(user):
    return Course.objects.create(title='Test Course', owner=user)

@pytest.fixture
def lesson(user, course):
    return Lesson.objects.create(title='Test Lesson', course=course, owner=user)

@pytest.mark.django_db
def test_user_can_view_courses(api_client, user, course):
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/courses/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_moderator_can_view_courses(api_client, moderator, course):
    api_client.force_authenticate(user=moderator)
    response = api_client.get('/api/courses/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_can_create_course(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/courses/', {
        'title': 'New Course',
        'description': 'Course Description'
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_moderator_cannot_create_course(api_client, moderator):
    api_client.force_authenticate(user=moderator)
    response = api_client.post('/api/courses/', {
        'title': 'New Course',
        'description': 'Course Description'
    })
    assert response.status_code == 403

@pytest.mark.django_db
def test_user_can_delete_own_course(api_client, user, course):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/courses/{course.id}/')
    assert response.status_code == 204

@pytest.mark.django_db
def test_moderator_cannot_delete_course(api_client, moderator, course):
    api_client.force_authenticate(user=moderator)
    response = api_client.delete(f'/api/courses/{course.id}/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_user_can_view_own_lessons(api_client, user, lesson):
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/lessons/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_moderator_can_view_all_lessons(api_client, moderator):
    api_client.force_authenticate(user=moderator)
    response = api_client.get('/api/lessons/')
    assert response.status_code == 200