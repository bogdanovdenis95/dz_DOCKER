from celery import shared_task
from django.core.mail import send_mail
from .models import Subscription

@shared_task
def send_course_update_email(course_id):
    subscriptions = Subscription.objects.filter(course_id=course_id)
    for subscription in subscriptions:
        print(subscription)
        send_mail(
            'Course Updated',
            'The course you are subscribed to has been updated.',
            'bogdanovskypro@yandex.ru',
            [subscription.user.email],
            fail_silently=False,
        )
