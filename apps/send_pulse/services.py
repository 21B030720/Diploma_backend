import logging
import random
import string

import requests
from django.db import transaction

from apps.send_pulse.models import UserCode
from config import settings


@transaction.atomic
def send_email_confirmation_message(user):
    token = get_token()
    if not token:
        logging.warning("Failed to authenticate with SendPulse")
        return
    confirmation_code = generate_confirmation_code(k=10)
    complete_registration_link = generate_complete_registration_link(user, confirmation_code)
    to_email = user.client_user.email
    logging.warning(to_email)
    email_data = {
        "email": {
            "subject": "Kampitik Confirmation Email",
            "from": {
                "name": "Kampitik",
                "email": "az_bazarbai@kbtu.kz"
            },
            "to": [
                {"email": user.client_user.email}
            ],
            "text": f"Hello! Thank you for registering in kampitik. "
                    f"To complete your registration, please go trough the link below: \n"
                    f"{complete_registration_link}"
        }
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(settings.SEND_PULSE_SMTP_URL, headers=headers, json=email_data)
    logging.warning(response)
    if response.status_code == 200:
        logging.info("Email sent successfully")
    else:
        logging.warning("Failed to send email:", response.json())


def generate_confirmation_code(k=10):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return code


def generate_complete_registration_link(user, confirmation_code):
    user_code = UserCode.objects.filter(user=user).first()
    if user_code:
        user_code.code = confirmation_code
        user_code.save(update_fields=["code"])
    else:
        UserCode.objects.create(user=user, code=confirmation_code)
    link = settings.BASE_URL + f"/emails/confirm-email/?code={confirmation_code}&user_id={user.id}"
    return link


def get_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": settings.SEND_PULSE_ID,
        "client_secret": settings.SEND_PULSE_SECRET
    }
    response = requests.post(settings.SEND_PULSE_TOKEN_URL, json=payload)
    return response.json().get("access_token")
