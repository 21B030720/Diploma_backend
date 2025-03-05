from rest_framework import serializers

from apps.paybox.models import Card


class InitPaymentSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()


class SavedCardPaymentSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    card_id = serializers.IntegerField()


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'card_hash',
            'card_month',
            'card_year',
            'default'
        )
