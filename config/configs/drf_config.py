REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Payouts Service API",
    "DESCRIPTION": "REST API for managing payout requests with async processing",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
