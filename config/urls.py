from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from payouts.api.views import PayoutViewSet

router = DefaultRouter()
router.register("payouts", PayoutViewSet, basename="payouts")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
            schema=None,
        ),
        name="swagger-ui",
    ),

    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
            schema=None,
        ),
        name="redoc",
    ),
]
