from rest_framework import serializers


class BadRequestSerializer(serializers.Serializer):
    detail = serializers.CharField()
