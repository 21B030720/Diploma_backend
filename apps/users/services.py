from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.users.models import User, CRMUser


@transaction.atomic
def create_user(data):
    user_data = data.get('user')
    username = user_data['username'].lower()
    password = user_data['password']

    existing_user = User.all_objects.filter(username__iexact=username).first()
    if existing_user is not None:
        if existing_user.deleted:
            existing_user.deleted = False
            existing_user.crm_user.deleted = False
            existing_user.save(update_fields=['deleted'])
            existing_user.crm_user.save(update_fields=['deleted'])
            crm_user = update_user(existing_user.crm_user.id, data)
            return crm_user
        else:
            raise ValidationError('Пользователь с таким логином уже существует.')
    else:
        user_data = data.pop('user', None)
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
