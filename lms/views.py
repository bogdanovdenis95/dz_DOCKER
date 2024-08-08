from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import CanViewAndEditOnly, IsModerator

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            if self.action in ['list', 'retrieve', 'update', 'partial_update']:
                return [IsAuthenticated(), CanViewAndEditOnly()]
            return [IsAuthenticated(), IsModerator()]  # Запретить создание и удаление
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Модераторы').exists():
            # Не допускаем создание объектов модераторами
            raise PermissionDenied("Вы не имеете права создавать курсы.")
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Модераторы').exists():
            # Запретить удаление
            raise PermissionDenied("Вы не имеете права удалять курсы.")
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            if self.action in ['list', 'retrieve', 'update', 'partial_update']:
                return [IsAuthenticated(), CanViewAndEditOnly()]
            return [IsAuthenticated(), IsModerator()]  # Запретить создание и удаление
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Модераторы').exists():
            # Не допускаем создание объектов модераторами
            raise PermissionDenied("Вы не имеете права создавать уроки.")
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Модераторы').exists():
            # Запретить удаление
            raise PermissionDenied("Вы не имеете права удалять уроки.")
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)
