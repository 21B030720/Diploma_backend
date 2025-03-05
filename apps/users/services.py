from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.users.models import User, CRMUser, ClientUser


@transaction.atomic
def create_user(data):
    user_data = data.get('user')
    username = user_data['username'].lower()
    password = user_data['password']

    existing_user = User.all_objects.filter(username__iexact=username).first()
    if existing_user is not None:
        raise ValidationError('Пользователь с таким логином уже существует.')
    else:
        user_data = data.pop('user')
        user_data['username'] = username
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        crm_user = CRMUser.objects.create(**data, user=user)
        return crm_user


def update_user(pk, data):
    crm_user = get_object_or_404(CRMUser, pk=pk)
    user = User.objects.get(pk=crm_user.user.pk)
    user_data = data.pop('user')
    username = user_data.pop('username', None)
    password = user_data.pop('password', None)

    existing_user = User.objects.filter(username__iexact=username).exclude(id=user.id).exists()
    if existing_user:
        raise ValidationError("User with that username already exists.")
    user.username = username.lower()
    user.set_password(password)
    user.save()
    for key, value in data.items():
        setattr(crm_user, key, value)

    crm_user.save()
    return crm_user


@transaction.atomic()
def create_client_user(data):
    user_data = data.get('user')
    username = user_data['username'].lower()
    password = user_data['password']

    existing_user = User.all_objects.filter(username__iexact=username).first()
    if existing_user is not None:
        raise ValidationError('User with this username already exists.')
    else:
        user_data = data.pop('user')
        user_data['username'] = username
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        validate_client_user(data)
        client_user = ClientUser.objects.create(**data, user=user)
        return client_user


def validate_client_user(client_data):
    email = client_data.get('email')
    phone_number = client_data.get('phone_number')
    existing_client_user = ClientUser.all_objects.filter(email__iexact=email).exists()
    if existing_client_user:
        raise ValidationError("Email is already taken.")

    existing_client_user = ClientUser.all_objects.filter(phone_number=phone_number).exists()
    if existing_client_user:
        raise ValidationError("Phone number is already taken.")
