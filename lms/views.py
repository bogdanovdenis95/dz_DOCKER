from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, CanViewAndEditOnly
from rest_framework.exceptions import PermissionDenied

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            if self.action in ['list', 'retrieve', 'update', 'partial_update']:
                return [IsAuthenticated(), CanViewAndEditOnly()]
            elif self.action in ['create', 'destroy']:
                return [IsAuthenticated(), IsModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("You are not allowed to create courses.")
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("You are not allowed to delete courses.")
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            if self.request.method == 'POST':
                return [IsAuthenticated(), IsModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("You are not allowed to create lessons.")
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            if self.request.method in ['GET', 'PUT', 'PATCH']:
                return [IsAuthenticated(), CanViewAndEditOnly()]
            elif self.request.method == 'DELETE':
                return [IsAuthenticated(), IsModerator()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("You are not allowed to delete lessons.")
        return super().perform_destroy(instance)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

