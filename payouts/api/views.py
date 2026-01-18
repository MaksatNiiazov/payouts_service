from drf_spectacular.openapi import AutoSchema
from rest_framework.viewsets import ModelViewSet

from payouts.models import Payout
from payouts.services import create_payout
from .serializers import (
    PayoutSerializer,
    PayoutCreateSerializer,
    PayoutStatusUpdateSerializer,
)


class PayoutViewSet(ModelViewSet):
    schema = AutoSchema()

    queryset = Payout.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "create":
            return PayoutCreateSerializer
        if self.action == "partial_update":
            return PayoutStatusUpdateSerializer
        return PayoutSerializer

    def perform_create(self, serializer):
        create_payout(data=serializer.validated_data)
