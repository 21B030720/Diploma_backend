from celery.app import shared_task

from apps.send_pulse.services import send_email_confirmation_message
from apps.users.models import User


@shared_task()
def send_pulse_email(user_id):
    user = User.objects.get(pk=user_id)
    send_email_confirmation_message(user)
