from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, SubscriptionView, CreatePaymentView, CreatePriceView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
    path('subscriptions/', SubscriptionView.as_view(), name='subscription'),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('create-price/', CreatePriceView.as_view(), name='create-price'),
]
