from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer

class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name='course__id')
    lesson = filters.NumberFilter(field_name='lesson__id')
    payment_method = filters.ChoiceFilter(field_name='payment_method', choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_date_gte = filters.DateTimeFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_lte = filters.DateTimeFilter(field_name='payment_date', lookup_expr='lte')
    ordering = filters.OrderingFilter(fields=('payment_date',))

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method', 'payment_date_gte', 'payment_date_lte']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
