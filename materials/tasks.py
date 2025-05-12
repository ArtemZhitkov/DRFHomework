from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from materials.models import Subscription
from users.models import User


@shared_task
def send_mail_about_course_update(course_id):
    """Отправляет письмо об изменении курса."""
    subscription_course = Subscription.objects.filter(course=course_id)
    recipient_list = [sub.user.email for sub in subscription_course]
    if recipient_list:
        subject = f"Изменение курса: {subscription_course.first().course.title}"
        message = f"Курс {subscription_course.first().course.title} был изменен."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )


@shared_task
def check_last_login():
    """Проверка последнего логина пользователя и блокировка его если пользователь не заходил более месяца"""
    users = User.objects.filter(last_login__isnll=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f"Пользователь {user.email} заблокирован")
