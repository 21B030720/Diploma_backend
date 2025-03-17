from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.users.kids.models import Kid, KidLevel
from apps.utils.enums import OrderItemStatus


def add_kid(client_user, data):
    first_kid_level = KidLevel.objects.order_by('level_position').first()
    kid = Kid.objects.create(**data, kid_level=first_kid_level, client_user=client_user)
    return kid


def update_kid(pk, data):
    kid = get_object_or_404(Kid, pk=pk)

    for key, value in data.items():
        setattr(kid, key, value)

    kid.save()
    return kid


def delete_kid(pk):
    kid = get_object_or_404(Kid, pk=pk)
    kid.deleted = True
    kid.save(update_fields=['deleted'])


def reupdate_kid(client_user, pk):
    kid = Kid.objects.filter(client_user=client_user, pk=pk).first()
    if not kid:
        raise ValidationError("This is not your kid! You cannot buy stuff for other kids except yours.")
    # order_items = kid.order_items.exclude(status=OrderItemStatus.CANCELLED)
    total_price = kid.xp
    if total_price > kid.kid_level.to_xp:
        kid_level = KidLevel.objects.filter(from_xp__lte=total_price, to_xp__gte=total_price).first()
        if kid_level is None:
            kid_level = KidLevel.objects.order_by('-level_position').first()

        kid.kid_level = kid_level

    kid.save(update_fields=['kid_level'])
