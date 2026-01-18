from rest_framework import serializers

from payouts.models import Payout, PayoutStatus

SUPPORTED_CURRENCIES = {"USD", "EUR", "KGS"}


class PayoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ("amount", "currency", "recipient_details", "comment")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate_currency(self, value):
        value = value.upper()
        if value not in SUPPORTED_CURRENCIES:
            raise serializers.ValidationError("Unsupported currency")
        return value

    def validate_recipient_details(self, value):
        value = value.strip()
        if not (8 <= len(value) <= 500):
            raise serializers.ValidationError("Invalid recipient details length")
        return value


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = "__all__"


class PayoutStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ("status",)

    def validate_status(self, value):
        allowed = {PayoutStatus.PROCESSING, PayoutStatus.FAILED}
        if value not in allowed:
            raise serializers.ValidationError("Invalid status transition")
        return value
