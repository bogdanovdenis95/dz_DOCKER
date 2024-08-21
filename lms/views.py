from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner, NotModerator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .paginators import CustomPagination
from .services import create_stripe_product, create_stripe_price, create_checkout_session
from rest_framework.exceptions import PermissionDenied


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
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("User is not authenticated")
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
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("User is not authenticated")
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
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("User is not authenticated")
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


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
    
class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        # Создаем продукт в Stripe
        product_id = create_stripe_product(course.title, course.description)
        
        # Создаем цену в Stripe
        price_id = create_stripe_price(product_id, course.price)
        
        # Создаем сессию оплаты в Stripe
        success_url = "https://example.com/success/"
        cancel_url = "https://example.com/cancel/"
        session = create_checkout_session(price_id, success_url, cancel_url)
        
        return Response({"checkout_url": session.url}, status=status.HTTP_200_OK)
    
class CreatePriceView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        amount = request.data.get('amount')
        
        if not product_id or not amount:
            return Response({"error": "Missing product_id or amount"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = int(amount)
        except ValueError:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            price_id = create_stripe_price(product_id, amount)
            return Response({"price_id": price_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
