from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.conf import settings
from lms.models import Course, Lesson

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    city = models.CharField(max_length=150, verbose_name='Город', null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('transfer', 'Bank Transfer'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment {self.id} by {self.user}"
