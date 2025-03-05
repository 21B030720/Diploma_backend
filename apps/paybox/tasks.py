from celery import shared_task
from requests import RequestException, Timeout, HTTPError

from apps.paybox.models import Card
from apps.paybox.services import delete_user_card
from apps.users.models import User


@shared_task(bind=True,
             autoretry_for=(Timeout, HTTPError, RequestException),
             retry_backoff=True,
             retry_kwargs={'max_retries': 3, 'countdown': 5})
def delete_user_card_task(self, user_id, card_id):
    user = User.objects.get(pk=user_id)
    card = Card.objects.get(pk=card_id)
    delete_user_card(user, card.card_token)
