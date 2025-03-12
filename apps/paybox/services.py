import base64
import hashlib
import logging
import secrets
from collections import OrderedDict
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs

import requests
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.paybox.models import Card
from apps.utils.enums import TransactionStatus
from apps.utils.services import only_digits_phone_number, convert_phone_number
from apps.wallets.models import Transaction
from apps.wallets.services import finish_transaction
from config import settings
from config.settings import env

secret_key_accepting = env('SECRET_KEY_FOR_ACCEPTING')
merchant_id = env('MERCHANT_ID')
paybox_base_url = env('PAYBOX_BASE_URL')


def generate_sign(data, sign_type):
    data = OrderedDict(sorted(data.items()))
    new_data = OrderedDict([(0, f'{sign_type}')] + list(data.items()) + [(1, secret_key_accepting)])
    return hashlib.md5(';'.join(str(i) for i in new_data.values()).encode('utf-8')).hexdigest()


def generate_salt(length=16):
    salt_bytes = secrets.token_bytes(length)
    salt_base64 = base64.b64encode(salt_bytes).decode('utf-8')
    return salt_base64


salt = generate_salt()


def start_init_payment(transaction_id):
    url = f'{paybox_base_url}/init_payment.php'
    transaction = Transaction.objects.get(id=transaction_id)
    client_user = transaction.wallet.client_user
    phone_number = str(client_user.phone_number)
    data = {
        'pg_order_id': transaction.id,
        'pg_salt': salt,
        'pg_merchant_id': merchant_id,
        'pg_amount': transaction.amount,
        'pg_description': f'Перевод денег: {phone_number}',
        'pg_currency': 'KZT',
        'pg_language': 'ru',
        'pg_testing_mode': '1',
        'pg_success_url': f'{settings.KAMPITIK_FRONT_URL}/en/payment-status/success',
        'pg_failure_url': f'{settings.KAMPITIK_FRONT_URL}/en/payment-status/failure',
        'pg_result_url': f'{settings.BASE_URL}/paybox/result/payment/',  # 8001 port for testing
        'pg_user_phone': f'{phone_number}',
        'pg_user_id': f'{client_user.user.id}'
    }
    data['pg_sig'] = generate_sign(data, 'init_payment.php')
    response = requests.post(url, data=data)
    xml_text = ET.fromstring(response.text)
    try:
        message = xml_text.find('pg_redirect_url').text, 200
    except Exception as e:
        message = xml_text.find('pg_error_description').text, 400
    return message


def pay_with_saved_card(card_id, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    card = Card.objects.get(id=card_id)
    client_user = transaction.wallet.client_user
    first_step_url = f'{paybox_base_url}/v1/merchant/{merchant_id}/card/init'
    phone_number = only_digits_phone_number(str(client_user.phone_number))
    phone_number = convert_phone_number(phone_number)

    first_step_post_data = {
        'pg_merchant_id': merchant_id,
        'pg_user_id': client_user.user.id,
        'pg_amount': transaction.amount,
        'pg_order_id': transaction.id,
        'pg_description': f'Перевод денег: {phone_number}',
        'pg_card_token': card.card_token,
        'pg_result_url': f'{settings.BASE_URL}/paybox/result/payment/',
        'pg_success_url': f'{settings.KAMPITIK_FRONT_URL}/en/payment-status/success',
        'pg_failure_url': f'{settings.KAMPITIK_FRONT_URL}/en/payment-status/failure',
        'pg_salt': salt,
    }
    first_step_post_data['pg_sig'] = generate_sign(first_step_post_data, 'init')
    first_step_response = requests.post(first_step_url, first_step_post_data)
    first_step_xml_text = ET.fromstring(first_step_response.text)

    pg_status = first_step_xml_text.find('pg_status').text
    if pg_status != 'ok':
        raise ValidationError('Payment status returned error')

    pg_payment_id = first_step_xml_text.find('pg_payment_id').text
    pg_salt = first_step_xml_text.find('pg_salt').text

    second_step_url = f'{paybox_base_url}/v1/merchant/{merchant_id}/card/pay'

    second_step_post_data = {
        'pg_merchant_id': merchant_id,
        'pg_payment_id': pg_payment_id,
        'pg_salt': pg_salt,
    }
    second_step_post_data['pg_sig'] = generate_sign(second_step_post_data, 'pay')
    second_step_response = requests.post(second_step_url, second_step_post_data)
    return second_step_response.text


def save_user_card(user):
    url = f'{paybox_base_url}/v1/merchant/{merchant_id}/cardstorage/add2'
    data = {
        'pg_merchant_id': merchant_id,
        'pg_user_id': user.id,
        'pg_salt': salt,
        'pg_post_link': f'{settings.BASE_URL}/paybox/result/card-save/',
        'pg_back_link': f'{settings.KAMPITIK_FRONT_URL}/en/cabinet'
    }
    data['pg_sig'] = generate_sign(data, 'add2')

    response = requests.post(url, data=data)

    xml_text = ET.fromstring(response.text)
    try:
        message = xml_text.find('pg_redirect_url').text, 200
    except Exception as e:
        message = xml_text.find('pg_error_description').text, 400
    return message


def delete_user_card(user, card_token):
    url = f'{paybox_base_url}/v1/merchant/{merchant_id}/cardstorage/remove'
    data = {
        'pg_merchant_id': merchant_id,
        'pg_user_id': user.id,
        'pg_card_token': card_token,
        'pg_salt': salt
    }

    data['pg_sig'] = generate_sign(data, 'remove')

    response = requests.post(url, data=data)

    if response.status_code == 200:
        logging.debug(f"Card was deleted successfully. User: {user.id}, Card_token: {card_token}")
    else:
        logging.warning(f"Card deletion request was returned with status: {response.status_code}. "
                        f"Request data: {data}, "
                        f"Response data: {response.text}")


def process_response(response):
    print('process_response function prints:')
    print(response)
    print(type(response))

    parsed_data = parse_qs(response)
    pg_result = int(parsed_data.get('pg_result', [None])[0])
    transaction_id = int(parsed_data.get('pg_order_id', [None])[0])

    transaction = Transaction.objects.get(id=transaction_id)
    if pg_result == 1:
        if transaction.status == TransactionStatus.PENDING:
            transaction.status = TransactionStatus.FINISHED
            transaction.save(update_fields=['status'])
            finish_transaction(transaction)
    else:
        transaction.status = TransactionStatus.CANCELED
        transaction.save(update_fields=['status'])

    return transaction
