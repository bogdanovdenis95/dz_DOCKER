from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner, NotModerator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .paginators import CustomPagination

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), IsModerator()]
            else:
                return [IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated(), NotModerator()]
        elif self.action == 'destroy':
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), NotModerator()]
            else:
                return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), NotModerator()]  # Обычные пользователи могут создавать
        return [IsAuthenticated()]  # Модераторы и обычные пользователи могут просматривать

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()  # Модераторы видят все уроки
        return Lesson.objects.filter(owner=self.request.user)  # Обычные пользователи видят только свои уроки

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), IsModerator()]  # Модераторы могут просматривать и редактировать
            return [IsAuthenticated(), IsOwner()]  # Обычные пользователи могут редактировать только свои уроки
        elif self.request.method == 'DELETE':
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), NotModerator()]  # Модераторы не могут удалять
            return [IsAuthenticated(), IsOwner()]  # Обычные пользователи могут удалять только свои уроки
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()  # Модераторы видят все уроки
        return Lesson.objects.filter(owner=self.request.user)  # Обычные пользователи видят только свои уроки


class SubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли уже подписка
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        
        if created:
            message = 'Subscription added'
        else:
            subscription.delete()
            message = 'Subscription removed'
        
        return Response({"message": message}, status=status.HTTP_200_OK)