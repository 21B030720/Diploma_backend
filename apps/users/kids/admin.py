from django.contrib import admin

from apps.users.kids.models import KidLevel


# Register your models here.
@admin.register(KidLevel)
class KidLevelAdmin(admin.ModelAdmin):
    list_display = ('level_name', 'level_position', 'level_image', 'from_xp', 'to_xp', 'created_at', 'changed_at')
    list_filter = ('level_position',)
    search_fields = ('level_name',)
    ordering = ('level_position',)
