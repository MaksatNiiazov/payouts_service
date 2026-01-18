from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payouts.api.views import PayoutViewSet

router = DefaultRouter()
router.register("payouts", PayoutViewSet, basename="payouts")

urlpatterns = [
    path("", include(router.urls)),
]
