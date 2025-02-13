from django.db import models

from apps.utils.managers import NotDeletedManager
from django.utils.translation import gettext_lazy as _


class DeletedMixin(models.Model):
    deleted = models.BooleanField(default=False)

    objects = NotDeletedManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        _("Время создания"), auto_now_add=True, db_index=True
    )
    changed_at = models.DateTimeField(
        _("Время последнего изменения"), auto_now=True, db_index=True
    )

    class Meta:
        abstract = True
