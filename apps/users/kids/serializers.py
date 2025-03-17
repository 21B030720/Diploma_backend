from rest_framework import serializers

from apps.users.kids.models import KidLevel, Kid


class KidLevelSerializer(serializers.ModelSerializer):
    next_level_position = serializers.SerializerMethodField()
    current_progress = serializers.SerializerMethodField()

    class Meta:
        model = KidLevel
        fields = (
            'id',
            'level_name',
            'level_image',
            'level_position',
            'from_xp',
            'to_xp',
            'next_level_position',
            'current_progress'
        )

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_next_level_position(self, obj):
        next_kid_level = KidLevel.objects.filter(level_position__gt=obj.level_position).order_by('level_position').first()
        return next_kid_level.level_position if next_kid_level else None

    def get_current_progress(self, obj):
        if not self.current_user and not hasattr(self.current_user, 'client_user'):
            return None

        current_kid = Kid.objects.filter(client_user=self.current_user.client_user).first()
        if not current_kid:
            return None
        current_xp_for_kid = current_kid.xp
        relative_current_xp = current_xp_for_kid - obj.from_xp
        relative_total_xp = obj.to_xp - obj.from_xp

        current_progress = (relative_current_xp / relative_total_xp) * 100

        if current_progress >= 100:
            return 100

        return round(current_progress, 2)


class KidSerializer(serializers.ModelSerializer):
    kid_level = KidLevelSerializer()

    class Meta:
        model = Kid
        fields = (
            'id',
            'image',
            'name',
            'age',
            'details',
            'xp',
            'kid_level'
        )


class KidCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Kid
        fields = (
            'name',
            'image',
            'age',
            'details'
        )
