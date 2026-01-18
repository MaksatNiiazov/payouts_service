import os
import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ.setdefault("DJANGO_DEBUG", "1")

    # Docker-only environment
    os.environ.setdefault("POSTGRES_DB", "payouts")
    os.environ.setdefault("POSTGRES_USER", "payouts")
    os.environ.setdefault("POSTGRES_PASSWORD", "payouts")
    os.environ.setdefault("POSTGRES_HOST", "db")
    os.environ.setdefault("POSTGRES_PORT", "5432")

    # Celery — eager mode for tests
    os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "1")
    os.environ.setdefault("CELERY_TASK_EAGER_PROPAGATES", "1")

    os.environ.setdefault("CELERY_BROKER_URL", "redis://redis:6379/0")
    os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://redis:6379/1")


@pytest.fixture
def api_client():
    return APIClient()
